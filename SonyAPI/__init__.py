# -*- coding: utf-8 -*-
#
# SonyAPI
# External control of Sony Bravia Generation 3 TV's
# Copyright (C) 2017  Kevin G. Schlosser
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
SonyAPI - Sony Bravia TV JSON API for Python 2.x and 3.x
This API works with generation 3 TV's. It is untested for generation 1 and 2.

I want to give mention to a couple of other authors for providing me with
ideas and insight on how to use some of the methods.

aparraga / braviarc
alanreid / bravia

"""

from __future__ import absolute_import
import threading
import base64
import sys
import json
import time
import socket
import struct
import requests
from .version import __version__, __version_info__, __author__
from . import (
    audio,
    access_control,
    app_control,
    av_content,
    broadcast_link,
    browser,
    cec,
    content_share,
    encryption,
    exception,
    guide,
    ir_command_proxy,
    notification,
    photo_share,
    recording,
    singleton,
    system,
    video_screen
)
from .logger import LOGGER as _LOGGER
from .utils import (
    get_mac_addresses as _get_mac_addresses,
    cache_icons as _cache_icons
)
from .exception import NoSuchMethodError


from .api_const import (
    GUID,
    VOLUME_EVENT,
    MUTE_EVENT,
    SOURCE_EVENT,
    CHANNEL_EVENT,
    POWER_EVENT,
    MEDIA_EVENT,
    SSDP_ADDR,
    SSDP_PORT,
    SSDP_MX,
    SSDP_ST,
    SSDP_REQUEST,
    HEADER,
    BODY,
    NUMBERS,
    PY30_31
)

try:
    __builtin__ = __import__('__builtin__')
except ImportError:
    __builtin__ = __import__('builtins')


SERVICE_MAPPINGS = dict(
    guide=['guide', guide.Guide],
    system=['system', system.System],
    videoScreen=['video_screen', video_screen.VideoScreen],
    audio=['audio', audio.Audio],
    avContent=['av_content', av_content.AVContent],
    recording=['recording', recording.Recording],
    appControl=['app_control', app_control.AppControl],
    browser=['browser', browser.Browser],
    notification=['notification', notification.Notification],
    cec=['cec', cec.CEC],
    accessControl=['access_control', access_control.AccessControl],
    irCommandProxy=['ir_command_proxy', ir_command_proxy.IRCommandProxy],
    encryption=['encryption', encryption.Encryption],
    photoShare=['photo_share', photo_share.PhotoShare],
    broadcastLink=['broadcast_link', broadcast_link.BroadcastLink],
    contentShare=['content_share', content_share.ContentShare]
)


def _build_command_list(device_url):

    methods = dict()

    url = device_url + '/guide'
    json_data = json.dumps({
        "id": 1,
        "method": "getSupportedApiInfo",
        "version": "1.0",
        "params": [{"service": []}]
    }).encode('UTF-8')

    response = requests.post(
        url,
        data=json_data
    ).content.decode('utf-8')

    response = json.loads(response)

    if 'error' in response and response['error'][0] == 12:
        url = device_url + 'guide'
        json_data = json.dumps({
            "id":      1,
            "method":  "getServiceProtocols",
            "version": "1.0",
            "params":  []
        }).encode('UTF-8')

        response = requests.post(
            url,
            data=json_data
        ).content.decode('utf-8')

        services = list(
            result[0] for result in json.loads(response)['results']
        )

        for service in services:
            methods[service] = dict()

            url = device_url + '/' + service
            json_data = json.dumps({
                "id":      1,
                "method":  "getMethodTypes",
                "version": "1.0",
                "params":  [""]
            }).encode('UTF-8')
            response = requests.post(
                url,
                data=json_data
            ).content.decode('utf-8')

            for method in json.loads(response)['results']:
                if method[0] in methods[service]:
                    methods[service][method[0]] = str(max(
                        float(method[3]),
                        float(methods[service][method[0]])
                    ))
                else:
                    methods[service][method[0]] = method[3]

    elif 'error' not in response:
        services = response['result'][0]

        for service in services:
            methods[service['service']] = {}
            for method in service['apis']:
                high_version = 0.0
                for ver in method['versions']:
                    high_version = max(
                        float(ver['version']),
                        high_version
                    )
                methods[service['service']][method['name']] = str(high_version)
    return methods


def discover(timeout=30.0):
    from xml.etree import cElementTree

    start_time = time.time()
    found_addresses = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    dest = socket.gethostbyname(SSDP_ADDR)
    sock.sendto(SSDP_REQUEST, (dest, SSDP_PORT))
    sock.settimeout(timeout)

    while time.time() - start_time < timeout:
        try:
            data = sock.recv(1000)
        except socket.timeout:
            break

        response = data.decode('utf-8')
        for line in response.split('\n'):
            line = line.strip()
            if not line:
                continue
            location = line.find('location:')

            if location > -1:
                url = line[location + 9:].strip()
                xml_data = requests.get(url).content
                from io import StringIO
                xml = StringIO(xml_data)

                namespaces = dict([
                    node for _, node in
                    cElementTree.iterparse(xml, events=['start-ns'])
                ])

                xml.close()
                xml_root = cElementTree.fromstring(xml_data)

                device_url = xml_root.find(
                    'X_ScalarWebAPI_BaseURL',
                    namespaces
                ).text

                if device_url not in found_addresses:
                    found_addresses += [device_url]
    _LOGGER.debug('||', found_addresses=found_addresses)

    devices = []
    for address in found_addresses:
        devices += [device(address)]

    return devices


def device(url):
    services = _build_command_list(url)

    class SonyAPI(SonyAPIBase):
        __metaclass__ = singleton.Singleton
        __services = services
        url = url


    for service_name, methods in services.items():
        service_name, service = SERVICE_MAPPINGS[service_name]

        class Service(service):
            __name__ = service.__name__

        for method in methods:
            method_name, method = Service.METHOD_MAPPINGS[method]
            Service.__dict__[method_name] = method

        def service_getter(self):
            if not hasattr(self, '__' + service_name):
                setattr(
                    self,
                    '__' + service_name,
                    Service(self)
                )
            return getattr(self, '__' + service_name)

        SonyAPI.__dict__[service_name] = property(fget=service_getter)


class SonyAPIBase(object):

    def __init__(
        self,
        ip_address=None,
        port=80,
        mac=None,
        nickname=None,
        pin=0000,
        psk=None,
        ssdp_timeout=10
    ):
        self._methods = {}
        self._remote_command_list = {}
        self._ircc_url = 'http://%s/sony/IRCC' % ip_address
        self._access_url = 'http://%s/sony/accessControl' % ip_address

        if ip_address is None:
            display_addresses = ''
            self._ip_address = None

            ip_addresses = SonyAPI.discover(ssdp_timeout)
            _get_mac_addresses(ip_addresses)
            _LOGGER.debug('||', ip_addresses=ip_addresses)

            for i, address in enumerate(sorted(ip_addresses.keys())):
                found_device = ip_addresses[address]
                if mac == found_device['mac']:
                    self._url = found_device['url']
                    ip_address, port = address
                    break
                else:
                    display_addresses += (
                        'Device {0}.)   {1}  -  {2}\n'.format(
                            i + 1, address[0], found_device['mac'])
                    )
            else:
                _LOGGER.debug('||', display_addresses=display_addresses)
                display_addresses += (
                    '\n\n Please input the number for '
                    'the TV you want to control.\n'
                )

                index = int(input(display_addresses))

                ip_address, port = sorted(ip_addresses.keys())[index - 1]
                self._url = ip_addresses[(ip_address, port)]['url']
        else:
            self._url = 'http://{0}:{1}/sony'.format(ip_address, port)

        self._ip_address = ip_address
        self._port = port
        _LOGGER.debug('||', ip_address=self._ip_address)

        if nickname is None:
            self._nickname = socket.gethostbyaddr(socket.gethostname())[0]
        else:
            self._nickname = nickname
        self._client_id = self._nickname + ':' + GUID

        self.icon_cache = {}
        self._icon_event = threading.Event()
        self._icon_thread = None
        self._cache_icons = False
        self._volume = None
        self._channel = 0
        self._cookies = None
        self._event_threads = []
        self._pin_timer = None
        self._timeout_event = None

        self._psk = psk
        if psk:
            self._pin = pin
            self._build_command_list()
        else:
            self._pin = None
            self.pin = pin

    def run_tests(self, enable_debugging=False):
        from . import test

        tmp_debug = _LOGGER.file_writer
        if enable_debugging:
            if not tmp_debug:
                _LOGGER.file_writer = sys.stdout.write
        else:
            _LOGGER.file_writer = None

        test.run(self)

        _LOGGER.file_writer = tmp_debug


    @staticmethod
    def debug(writer):
        if writer in (False, None):
            _LOGGER.file_writer = None
        elif writer is True:
            _LOGGER.file_writer = sys.stdout.write
        elif hasattr(writer, 'write'):
            _LOGGER.file_writer = writer.write
        elif PY30_31 and hasattr(writer, '__call__'):
            _LOGGER.file_writer = writer
        elif not PY30_31 and __builtin__.callable(writer):
            _LOGGER.file_writer = writer
        else:
            _LOGGER.file_writer = None

    @property
    def pin(self):
        return self._pin

    @pin.setter
    def pin(self, pin):
        params = [{
            'clientid': self._client_id,
            'nickname': self._nickname,
            'level': 'private'
        }]
        params += [[{'value': 'yes', 'function': 'WOL'}]]
        authorization = {
            'method': 'actRegister',
            'id': 1,
            'version': '1.0',
            'params': params
        }
        authorization = json.dumps(authorization).encode('utf-8')
        _LOGGER.debug('||', authorization=authorization)

        if pin:
            if self._pin_timer is not None:
                self._timeout_event.set()
                self._pin_timer.join(1.0)
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

        _LOGGER.debug('||', headers=headers)
        _LOGGER.debug(
            '<<',
            access_url=self._access_url,
            authorization=authorization,
            headers=headers
        )

        response = requests.post(
            self._access_url,
            data=authorization,
            headers=headers
        )
        json_data = response.json()
        _LOGGER.debug('>>', json_data)

        err = json_data.get('error', None)
        if err is not None:
            err_id = err[0]
            if err_id == 401 and not pin:
                timed_out = False
                self._timeout_event = threading.Event()

                def register_timeout():
                    global timed_out
                    self._timeout_event.wait(60000)

                    if not self._timeout_event.isSet():
                        timed_out = True
                        _LOGGER.error(err='RegisterTimeoutError')
                        raise exception.EXCEPTIONS[err_id](err)

                threading.Thread(target=register_timeout)

                self._pin_timer = threading.Thread(target=register_timeout)
                self._pin_timer.start()
                pin = input('Enter the pin that is seen on the TV')

            if pin and not timed_out:
                    self.pin = pin
            else:
                raise exception.EXCEPTIONS[err_id](err, json_data)

        self._cookies = response.cookies
        self._pin = pin
        self._build_command_list()

    def is_connected(self):
        return self._cookies is not None

    def _wake_on_lan(self):
        _LOGGER.debug('WOL ' + self.wol_mac)

        address_byte = tuple(
            int(b, 16) for b in self.wol_mac.split(':')
        )
        _LOGGER.debug(address_byte)

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
        response = requests.post(
            self._ircc_url,
            headers=HEADER,
            cookies=self._cookies,
            data=(BODY % code).encode('UTF-8')
        )
        content = response.content
        _LOGGER.debug('>>', content)
        return content

    def send(self, protocol, method, return_index=0, **params):
        try:
            methods = self._methods[protocol]
        except KeyError:
            raise exception.EXCEPTIONS[503]([503, "Service Unavailable"])

        try:
            found_version = methods[method]
        except KeyError:
            raise exception.EXCEPTIONS[501]([501, "Not Implemented"])

        if not params:
            params = [found_version]
            found_version = '1.0'
        else:
            params = [params]

        data = {
            'method': method,
            'params': params,
            'id': 1,
            'version': found_version
        }

        _LOGGER.debug('||', json_data=data)

        if self._psk is None:
            header = dict(cookies=self._cookies)
        else:
            header = dict(headers={'X-Auth-PSK': self._psk})

        header['data'] = json.dumps(data).encode('UTF-8')

        _LOGGER.debug('||', header=header)
        url = 'http://%s/sony/%s' % (self._ip_address, protocol)
        _LOGGER.debug('<<', url=url, header=header)
        response = requests.post(url, **header)
        response = json.loads(response.content.decode('utf-8'))
        _LOGGER.debug('>>', response=response)

        err = response.get('error', None)

        if err is not None:
            raise exception.EXCEPTIONS[err[0]](err)

        if isinstance(response['result'], list):
            return response['result'][return_index]
        else:
            return response['result']

    @property
    def cache_icons(self):
        return self._cache_icons

    @cache_icons.setter
    def cache_icons(self, flag):
        if self._icon_thread is not None and self._icon_thread.isAlive():
            self._icon_event.set()
            self._icon_thread.join(3.0)

        self._cache_icons = flag
        self.icon_cache.clear()

        if flag:
            self._icon_event.clear()
            self._icon_thread = threading.Thread(
                target=_cache_icons,
                args=(self, self._icon_event
                )
            )

    @property
    def channel(self):
        if not self._channel:
            self._channel = channel.Channels(self)
        return self._channel

    @channel.setter
    def channel(self, value):
        if isinstance(value, media.ContentItem):
            if 'tv' in value.uri:
                value.set()
        else:
            self.channel += int(value)

    def reboot(self):
        self.send('system', 'requestReboot')

    @property
    def command_list(self):
        return list(self._command_list.keys())

    @property
    def _command_list(self):
        if not self._remote_command_list:
            result = self.send(
                'system',
                'getRemoteControllerInfo',
                return_index=1
            )

            self._remote_command_list = dict(list(
                (command['name'], command['value'])
                for command in result
            ))
        return self._remote_command_list

    def refresh_command_list(self):
        self._remote_command_list = {}
        return self._command_list

    def send_command(self, command_name):
        try:
            self.ircc(self._command_list[command_name])
        except KeyError:
            raise SonyAPI.CommandError(
                'This device does not support command ' + command_name
            )

    @property
    def volume_data(self):
        return self.send('audio', 'getVolumeInformation')

    @property
    def power(self):
        response = self.send('system', 'getPowerStatus')
        return response['status'] == 'active'

    @power.setter
    def power(self, state):
        if state and not self.power:
            try:
                self.send_command('TvPower')
                self.send('system', 'setPowerStatus', status='true')
            except (SonyAPI.CommandError, SonyAPI.JSONRequestError):
                pass

            if not self.power:
                if not self.wol_mode:
                    self.wol_mode = True
                self._wake_on_lan()

        elif not state and self.power:
            self.send_command('PowerOff')

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


if __name__ == '__main__':
    print(
        "SonyAPI v%s, Copyright (C) 2017 Kevin G Schlosser.\n"
        "SonyAPI comes with ABSOLUTELY NO WARRANTY.\n"
        "SonyAPI is free software, and you are welcome to redistribute it"
        "under certain conditions." % __version__
    )
