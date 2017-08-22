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


import threading
import base64
import collections
import json
import socket
import struct
import requests
import traceback
from volume import Volume
from media import Media


VOLUME_EVENT = 0x1
MUTE_EVENT = 0x2
SOURCE_EVENT = 0x3
CHANNEL_EVENT = 0x4
POWER_EVENT = 0x5
MEDIA_EVENT = 0x6

ANY = '0.0.0.0'
MCAST_ADDR = '239.255.255.250'
MCAST_PORT = 1900

HEADER = dict(
    SOAPACTION='"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"'
)

BODY = (
    '<?xml version="1.0"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap'
    '/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><'
    's:Body><u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1"><IRCCC'
    'ode>%s</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>'
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
    file_writer = None

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

    def __init__(self, ip_address, pin=0000, psk=None, debug=None):
        _LOGGER.file_writer = debug

        self._ircc_url = 'http://%s/sony/IRCC' % ip_address
        self._access_url = 'http://%s/sony/accessControl' % ip_address
        self._ip_address = ip_address
        self._thread = None
        self._thread_event = threading.Event()
        self._callbacks = []
        self._cookies = None
        self._commands = []
        self._content_mapping = []
        self._pin_timer = None
        self._guid = '24F26C67-5A50-4B08-8754-80EBAF880379'
        self._pin = None
        self.media = None
        self._psk = psk
        self.pin = pin

    @property
    def pin(self):
        return self._pin

    @pin.setter
    def pin(self, pin):
        if self._psk is not None:
            self.media = Media(self)
            self._refresh_volume_devices()
            return

        nickname = socket.gethostbyaddr(socket.gethostname())[0]
        client_id = nickname + ':' + self._guid
        _LOGGER.debug(clientid)

        authorization = json.dumps({
            'method': 'actRegister',
            'id': 1,
            'version': '1.0',
            'params': [
                dict(
                    clientid=client_id,
                    nickname=nickname,
                    level='private'
                ),
                [dict(value='yes', function='WOL')]
            ],
        }).encode('utf-8')

        _LOGGER.debug(authorization)

        if pin:
            if self._pin_timer is not None:
                self._pin_timer.Stop()
                self._pin_timer = None

            base64string = base64.encodestring(
                ('%s:%s' % ('', pin)).encode()
            )
            headers = dict(
                Authorization=(
                    'Basic ' + base64string.decode().replace('\n', '')
                ),
                Connection='keep-alive'
            )
        else:
            headers = dict()

        _LOGGER.debug(headers)

        try:
            response = requests.post(
                self._access_url,
                data=authorization,
                headers=headers
            )
            response.raise_for_status()
            json_data = response.json()
            _LOGGER.debug(json_data)

            if json_data and json_data.get('error'):
                _LOGGER.debug(json_data)
                raise SonyAPI.JSONRequestError(json_data)

            self._cookies = response.cookies
            self._pin = pin
            self.media = Media(self)
            self._refresh_volume_devices()

        except requests.exceptions.HTTPError as exception_instance:
            if '401' in str(exception_instance):
                if pin:
                    raise SonyAPI.PinError(
                        'This device is not registered or the PIN is '
                        'invalid.\n\n' +
                        traceback.format_exc()
                    )
                else:
                    timed_out = False

                    def register_timeout():
                        global timed_out

                        timed_out = True

                        raise SonyAPI.RegisterTimeoutError(
                            'Registration time has expired'
                        )

                    self._pin_timer = wx.CallLater(60000, register_timeout)
                    self._pin_timer.Start()
                    pin = raw_input('Enter the pin that is seen on the TV')

                    if pin and not timed_out:
                        self.pin = pin
            else:
                raise SonyAPI.RegisterError(
                    'Unknown HTTP Error: ' + traceback.format_exc()
                )

        except requests.exceptions.RequestException:
            raise SonyAPI.RegisterError(
                'Unknown Request Error: ' + traceback.format_exc()
            )

    def is_connected(self):
        return self._cookies is not None

    def _wake_on_lan(self):
        _LOGGER.debug('WOL ' + self.mac_address)

        address_byte = tuple(
            int(b, 16) for b in self.mac_address.split(':')
        )
        _LOGGER.debug(addr_byte)

        hw_address = struct.pack('BBBBBB', *address_byte)
        msg = b'\xff' * 6 + hw_address * 16
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
            {'method': method, 'params': params, 'id': 1, 'version': '1.0'}
        )

        try:

            if self._psk is None:
                header = dict(cookies=self._cookies)
            else:
                header = dict(headers={'X-Auth-PSK': self._psk})

            response = requests.post(
                'http://%s/%s' % (self._ip_address, url),
                data=json_data.encode('UTF-8'),
                **header,
                )
            response = json.loads(response.content.decode('utf-8'))

            if response.get('error'):
                raise SonyAPI.JSONRequestError(response)
            return response

        except requests.exceptions.RequestException:
            raise SonyAPI.SendError(traceback.format_exc())

    @property
    def system_info(self):
        response = self.send('sony/system', 'getSystemInformation')
        return response['result'][0]

    @property
    def name(self):
        return self.system_info['name']

    @property
    def model(self):
        return self.system_info['model']

    @property
    def language(self):
        return self.system_info['language']

    @property
    def network_settings(self):
        resp = self.send('sony/system', 'getNetworkSettings')
        if resp is not None and not resp.get('error'):
            network_content_data = resp.get('result')[0]
            return network_content_data[0]

    @property
    def mac_address(self):
        return self.network_settings['hwAddr']

    @property
    def ip_address(self):
        return self.network_settings['ipAddrV4']

    '/sony/IRCC'
    '/sony/accessControl'
    '/sony/system'
    '/sony/avContent'
    '/sony/audio'
    '/sony/recording'
    '/sony/browser'
    '/sony/appControl'

    def _get_source(self, source):
        original_content_list = []
        content_index = 0
        while True:
            try:
                response = self.send(
                    'sony/avContent',
                    'getContentList',
                    source=source,
                    stIdx=content_index
                )
            except SonyAPI.JSONRequestError:
                break

            else:
                result = response['result'][0]
                if not len(result):
                    break

                _LOGGER.debug(result)
                content_index = result[-1]['index'] + 1
                original_content_list += result

        return original_content_list

    @property
    def channel_linup(self):
        result = {}
        for source in ['tv:dvbc', 'tv:dvbt']:
            content = self._get_source(source)
            if content:
                result[source] = content
        return result

    @property
    def source_list(self):
        original_content_list = []

        try:
            response = self.send(
                'sony/avContent',
                'getSourceList',
                scheme='tv'
            )
            results = response['result'][0]
            _LOGGER.debug(results)

            for result in results:
                if result['source'] in ['tv:dvbc', 'tv:dvbt']:
                    original_content_list += self._get_source(result['source'])
        except SonyAPI.JSONRequestError:
            pass

        try:
            response = self.send(
                'sony/avContent',
                'getSourceList',
                scheme='extInput'
            )
            results = response['result'][0]
            _LOGGER.debug(results)
            for result in results:
                if result['source'] == 'extInput:hdmi':
                    try:
                        response = self.send(
                            'sony/avContent',
                            'getContentList',
                            source='extInput:hdmi'
                        )
                        original_content_list += response['result'][0]
                    except SonyAPI.JSONRequestError:
                        continue
        except SonyAPI.JSONRequestError:
            pass

        return_value = collections.OrderedDict()
        for content_item in original_content_list:
            return_value[content_item['title']] = content_item['uri']
        return return_value

    @property
    def command_list(self):
        return list(self._command_list.keys())

    @property
    def _command_list(self):

        response = self.send('sony/system', 'getRemoteControllerInfo')

        return dict(list(
            (command['name'], command['value'])
            for command in response['result'][1]
        ))

    def send_command(self, command_name):
        try:
            self.ircc(self._command_list[command_name])
        except KeyError:
            raise SonyAPI.CommandError(
                'This device does not support command ' + command_name
            )

    def get_volume_data(self, device_name=None):
        response = self.send('sony/audio', 'getVolumeInformation')

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
            setattr(self, target, Volume(self, target))

    @property
    def power(self):
        response = self.send('sony/system', 'getPowerStatus')

        if response is None:
            raise SonyAPI.UnknownError()

        return response['result'][0]['status'] == 'active'

    @power.setter
    def power(self, state):
        if state and not self.power:
            try:
                self.send_command('TvPower')
                self.send('sony/system', 'setPowerStatus', status='true')
            except (SonyAPI.CommandError, SonyAPI.JSONRequestError):
                pass

            if not self.power:
                self._wake_on_lan()

        elif not state and self.power:
            self.send_command('PowerOff')

    @property
    def channel(self):
        return self.media.title

    @channel.setter
    def channel(self, channel):
        channel = str(channel)
        for char in channel:
            if char == '.':
                self.send_command('DOT')

            elif char.isdigit():
                self.send_command(NUMBERS[int(char)])

    @property
    def source(self):
        return self.media.source

    @source.setter
    def source(self, source):
        self.media.source = source

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item in self.command_list:
            def send_wrapper():
                if self.power:
                    self.send_command(item)

            setattr(self, item, send_wrapper)
            return send_wrapper

        raise AttributeError(
            '%s.%s does not have attribute %s' %
            (__name__, self.__class__.__name__, item)
        )

    def _event_loop(self):
        volume_devices = [
            getattr(self, volume_name)
            for volume_name in sorted(self.get_volume_data().keys())
        ]

        def get_volume_data():
            res = {}
            for volume_device in volume_devices:
                res[volume_device.name] = dict(
                    volume=volume_device.volume,
                    mute=volume_device.mute
                )
            return res

        old_power = self.power
        old_source = self.source
        old_title = self.media.title
        old_volume_data = get_volume_data()

        while not self._thread_event.isSet():
            events = []
            new_power = self.power

            if new_power != old_power:
                events += [POWER_EVENT]
                old_power = new_power

            new_source = self.source
            if new_source != old_source:
                events += [SOURCE_EVENT]
                old_source = new_source

            new_title = self.media.title

            if new_title != old_title:
                events +=[MEDIA_EVENT]
                old_title = new_title

            new_volume_data = get_volume_data()
            if new_volume_data != old_volume_data:
                for name in sorted(new_volume_data.keys()):
                    new_volume = new_volume_data[name]
                    old_volume = old_volume_data[name]
                    if new_volume != old_volume:
                        if new_volume['mute'] != old_volume['mute']:
                            events += [MUTE_EVENT]
                        if new_volume['volume'] != old_volume['volume']:
                            events += [VOLUME_EVENT]

                old_volume_data = new_volume_data

            for callback in self._callbacks:
                for event in events:
                    callback(event)

            self._thread_event.wait(0.2)

        self._thread = None

    def register_event_callback(self, callback):
        self._callbacks += [callback]

        if self._thread is None:
            self._thread_event.clear()
            self._thread = threading.Thread(
                target=self._event_loop,
                name=self.name + ': ' + self.model
            )

    def unregister_event_callback(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)

        if not self._callbacks:
            self._thread_event.set()
            self._thread.join(1.0)

    def discover(self):
        result = []
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
            socket.IPPROTO_UDP
        )
        sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )
        sock.bind((ANY, 6000))
        sock.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_MULTICAST_TTL,
            2
        )

        sock.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(MCAST_ADDR) + socket.inet_aton(ANY)
        )

        d_request = [
            'M-SEARCH * HTTP/1.1',
            'HOST: 239.255.255.250:1900',
            'MAN: "ssdp:discover"',
            'ST: urn:schemas-sony-com:service:IRCC:1',
            'MX: 3',
            ''
        ]

        sock.sendto('\r\n'.join(d_request), (MCAST_ADDR, MCAST_PORT))

        start_time = int(time.time())

        sock.setblocking(0)

        while (int(time.time()) - start_time) <= 30:
            try:
                data, addr = sock.recvfrom(4096)
            except socket.error:
                pass
            else:
                data_dict = dict()
                for d in data.decode('utf-8').rstrip().split('\r\n')[1:]:
                    key, value = d.split(':', 1)
                    data_dict[key] = value
                result += [data_dict]
        return result


# (@"http://" + mDev.IPAddress + @"/sony/system" "{\"id\":19,\"method\":\"getSystemSupportedFunction\",\"version\":\"1.0\",\"params\":[]}\""



# import SonyAPI
#
# sony_api = SonyAPI.SonyAPI('IP ADDRESS')
# sony_api.pin = 0000
# sony_api.pin = int(input('Enter Pin displayed on TV'))
#
# SonyAPI.run_tests(sony_api)




