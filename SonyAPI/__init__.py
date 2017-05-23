# SonyAPI
# Copyright (C) 2017 Kevin Schlosser

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import base64
import collections
import json
import socket
import struct
import ctypes
import requests
import traceback
from _utils import get_macaddress
from _volume_device import VolumeDevice


HEADER = dict(
    SOAPACTION='"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"'
)

BODY = (
    '<?xml version="1.0"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap'
    '/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><'
    's:Body><u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1"><IRCCC'
    'ode>%s</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>'
)

PLAYING_KEYS = (
    'programTitle',
    'title',
    'programMediaType',
    'dispNum',
    'source',
    'uri',
    'durationSec',
    'startDateTime'
)

NUMBERS = [
    'Num0'
    'Num1'
    'Num2'
    'Num3'
    'Num4'
    'Num5'
    'Num6'
    'Num7'
    'Num8'
    'Num9'
]


class _LOGGER:
    file_writer = False

    @classmethod
    def error(cls, err, data):
        if isinstance(data, dict):
            data = json.dumps(data, indent=4)

        if cls.file_writer:
            cls.file_writer.write(
                '%s.%s: %s\n' % (__name__, err, str(data))
            )

    @classmethod
    def debug(cls, data):
        if isinstance(data, dict):
            data = json.dumps(data, indent=4)

        if cls.file_writer:
            cls.file_writer.write(
                '%s: DEBUG: %s\n' % (__name__, str(data))
            )


class SonyAPIError(Exception):

    def __init__(self, msg):
        if isinstance(msg, dict):
            msg = json.dumps(msg, indent=4)

        _LOGGER.error(self.__class__.__name__, msg)
        self.msg = msg

    def __str__(self):
        return self.msg


class SonyAPI(object):

    class PinError(SonyAPIError):
        pass

    class RegisterTimeoutError(SonyAPIError):
        pass

    class JSONRequestError(SonyAPIError):
        pass

    class CommandError(SonyAPIError):
        pass

    class VolumeDeviceError(SonyAPIError):
        pass

    class RegisterError(SonyAPIError):
        pass

    class IRCCError(SonyAPIError):
        pass

    class SendError(SonyAPIError):
        pass

    def __init__(self, ip_address, debug=None):
        _LOGGER.file_writer = debug

        self._ircc_url = 'http://%s/sony/IRCC' % ip_address
        self._access_url = 'http://%s/sony/accessControl' % ip_address
        self._ip_address = ip_address
        self._cookies = None
        self._commands = []
        self._content_mapping = []
        self._pin_timer = None

    def connect(self, pin):
        fqdn = socket.gethostbyaddr(socket.gethostname())[0]
        mac = '-'.join(get_mac_address(socket.gethostbyname(fqdn)))
        clientid = fqdn + ':' + mac
        nickname = fqdn
        _LOGGER.debug(clientid)

        params_1 = dict(clientid=clientid, nickname=nickname, level="private"),
        params_2 = dict(value="yes", function="WOL")
        json_data = dict(
            method="actRegister",
            params=[params_1, [params_2]],
            id=13,
            version="1.0"
        )

        authorization = json.dumps(json_data).encode('utf-8')

        if pin:
            if self._pin_timer is not None:
                self._pin_timer.Stop()
                self._pin_timer = None

            pin = ('%s:%s' % ('', pin)).encode()
            base64string = base64.encodestring(pin).decode().replace('\n', '')
            headers = dict(
                Authorization="Basic %s" % base64string,
                Connection="keep-alive"
            )
        else:
            headers = dict()

        try:
            response = requests.post(
                self._access_url,
                data=authorization,
                headers=headers
            )
            response.raise_for_status()
            json_data = response.json()
            _LOGGER.debug(json_data)

            if json_data and json_data['error']:
                raise SonyAPI.JSONRequestError(json_data)

            elif json_data is None:
                self._cookies = response.cookies
                return True

        except requests.exceptions.HTTPError as exception_instance:
            if '401' in str(exception_instance):
                if Pin:
                    _LOGGER.error("[W] HTTPError: ", exception_instance)
                    raise SonyAPI.PinError(
                        'This device is not Registered or the PIN is invalid'
                    )
                else:
                    self._pin_timer = wx.CallLater(
                        6000,
                        SonyAPI.RegisterTimeoutError,
                        'Registration time has expired'
                    )
                    self._pin_timer.Start()
                    return None

            else:
                raise SonyAPI.RegisterError(traceback.format_exc())

        except requests.exceptions.RequestException:
            raise SonyAPI.RegisterError(traceback.format_exc())

        return False

    def is_connected(self):
        return self._cookies is not None

    def _wakeonlan(self):
        _LOGGER.debug('WOL ' + ':'.join(get_mac_address(self._ip_address)))

        addr_byte = tuple(
            int(b, 16) for b in get_mac_address(self._ip_address)
        )
        _LOGGER.debug(addr_byte)

        hw_addr = struct.pack('BBBBBB', *addr_byte)
        msg = b'\xff' * 6 + hw_addr * 16
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_BROADCAST,
            1
        )

        sock.sendto(msg, ('<broadcast>', 9))
        sock.close()
        _LOGGER.debug('WOL Packet Sent')

    def ircc(self, code):
        try:
            response = requests.post(
                self._ircc_url,
                headers=HEADER,
                cookies=self._cookies,
                data=(BODY % code).encode('UTF-8')
            )
            content = response.content
            return content

        except requests.exceptions.RequestException:
            raise SonyAPI.IRCCError(traceback.format_exc())

    def send(self, url, method, **params):
        if not params:
            params = []
        else:
            params = [params]

        json_data = json.dumps(
            dict(method=method, params=params, id=1, version="1.0")
        )

        try:
            response = requests.post(
                'http://%s/%s' % (self._ip_address, url),
                data=json_data.encode("UTF-8"),
                cookies=self._cookies,
                )
            return json.loads(response.content.decode('utf-8'))

        except requests.exceptions.RequestException:
            raise SonyAPI.SendError(traceback.format_exc())

    def _get_source(self, source):
        original_content_list = []
        content_index = 0
        while True:
            response = self.send(
                "sony/avContent",
                "getContentList",
                source=source,
                stIdx=content_index
            )

            if response['error'] or len(response['result'][0]) == 0:
                break

            result = response['result'][0]
            _LOGGER.debug(result)
            content_index = result[-1]['index'] + 1
            original_content_list += result

        return original_content_list

    @property
    def source_list(self):
        original_content_list = []

        response = self.send("sony/avContent", "getSourceList", scheme="tv")

        if not response['error']:
            results = response['result'][0]
            _LOGGER.debug(results)

            for result in results:
                if result['source'] in ['tv:dvbc', 'tv:dvbt']:
                    original_content_list += self.get_source(result['source'])

        response = self.send(
            "sony/avContent",
            "getSourceList",
            scheme="extInput"
        )

        if not response['error']:
            results = response['result'][0]
            _LOGGER.debug(results)
            for result in results:
                if result['source'] == 'extInput:hdmi':
                    response = self.send(
                        "sony/avContent",
                        "getContentList",
                        source="extInput:hdmi"
                    )

                    if not response['error']:
                        original_content_list += response['result'][0]

        return_value = collections.OrderedDict()
        for content_item in original_content_list:
            return_value[content_item['title']] = content_item['uri']
        return return_value

    @property
    def command_list(self):
        response = self.send("sony/system", "getRemoteControllerInfo")

        if response['error']:
            raise SonyAPI.JSONRequestError(response)

        return dict(list(
            (command['name'], command['value'])
                for command in response['result'][1]
        ))

    def send_command(self, command_name):
        try:
            self.ircc(self.command_list[command_name])
        except KeyError:
            raise SonyAPI.CommandError(
                'This device does not support command ' + command_name
            )

    def get_volume_data(self, device_name=None):
        response = self.send("sony/audio", "getVolumeInformation")

        if response['error']:
            raise SonyAPI.JSONRequestError(response)

        devices = dict(list(
            (device['target'], device)
            for device in response['result'][0]
        ))

        if device_name is None:
            return devices

        try:
            return devices[device_name]
        except KeyError:
            raise SonyAPI.VolumeDeviceError(
                'Device %s does not exist.' % device_name
            )

    def _refresh_volume_devices(self):
        for target in self.get_volume_data().keys():
            setattr(self, target, VolumeDevice(self, target))

    @property
    def power(self):
        response = self.send("sony/system", "getPowerStatus")
        if response['error']:
            raise SonyAPI.JSONRequestError(response)

        elif response is None:
            raise SonyAPI.UnknownError()

        return response['result'][0]['status'] == 'active'

    @power.setter
    def power(self, state):
        if state and not self.power:
            self._wakeonlan()

        elif not state and self.power:
            self.send_command('PowerOff')

    def _playing_info(self):
        response = self.send("sony/avContent", "getPlayingContentInfo")

        if response is not None and not response['error']:
            playing_content_data = response['result'][0]

            return dict(list(
                (key, playing_content_data[key]) for key in PLAYING_KEYS
            ))

        return dict()

    @property
    def source(self):
        return self._playing_info()['title']


    @property
    def channel(self):
        return self._playing_info()['title']


    @channel.setter
    def channel(self, channel):
        channel = str(channel)
        for char in channel:
            if char == '.':
                self.send_command('DOT')

            elif char.isdigit():
                self.send_command(NUMBERS[int(char)])

    @property
    def media(self):
        return self._playing_info()['title']

    @media.setter
    def media(self, title):
        self.power = True
        for source in self.source_list:
            if source['title'] == title:
                self.send(
                    "sony/avContent",
                    "setPlayContent",
                    uri=source['uri']
                )

    @source.setter
    def source(self, source):
        self.power = True
        source_list = self.source_list
        if source in source_list:
            self.media = source_list[source]

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item in self.command_list:
            def send_wrapper(self):
                if self.power:
                    self.send_command(item)

            setattr(self, item, send_wrapper)
            return send_wrapper

        raise AttributeError(
            '%s.%s does not have attribute %s' %
            (__name__, self.__class__.__name__, item)
        )

# (@"http://" + mDev.IPAddress + @"/sony/system" "{\"id\":19,\"method\":\"getSystemSupportedFunction\",\"version\":\"1.0\",\"params\":[]}\""
