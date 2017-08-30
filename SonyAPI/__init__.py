# -*- coding: utf-8 -*-
#
#  SonyAPI
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
import re
import json
import time
import socket
import struct
import ctypes
import requests
import traceback
import application
import volume
import media
import recording
import browser
import inputs
import channel
import speaker
from datetime import datetime
from utils import get_icon

VOLUME_EVENT = 0x1
MUTE_EVENT = 0x2
SOURCE_EVENT = 0x3
CHANNEL_EVENT = 0x4
POWER_EVENT = 0x5
MEDIA_EVENT = 0x6

SSDP_ADDR = "239.255.255.250"
SSDP_PORT = 1900
SSDP_MX = 1
SSDP_ST = "urn:schemas-sony-com:service:ScalarWebAPI:1"

SSDP_REQUEST = (
    'M-SEARCH * HTTP/1.1\r\n'
    'HOST: %s:%d\r\n'
    'MAN: "ssdp:discover"\r\n'
    'MX: %d\r\n'
    'ST: %s\r\n'
    '\r\n' % (SSDP_ADDR, SSDP_PORT, SSDP_MX, SSDP_ST)
)

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


def _get_mac_address(ip_address):
    send_arp = ctypes.windll.Iphlpapi.SendARP
    inetaddr = ctypes.windll.wsock32.inet_addr(ip_address)

    hw_address = ctypes.c_buffer(6)
    addlen = ctypes.c_ulong(ctypes.sizeof(hw_address))

    send_arp(inetaddr, 0, ctypes.byref(hw_address), ctypes.byref(addlen))

    res = []

    for val in struct.unpack('BBBBBB', hw_address):
        if val > 15:
            replace_str = '0x'
        else:
            replace_str = 'x'

        res.append(hex(val).replace(replace_str, '').upper())

    return ':'.join(res)


def cache_icons(sony_api):
    applications = sony_api.send('appControl', 'getApplicationList')
    for app in applications[:]:
        icon = app['icon']
        if (
            icon and
            sony_api._ip_address.split(':')[0] not in icon and
            icon not in sony_api.icon_cache
        ):
            def g_icon():
                try:
                    sony_api.icon_cache[icon] = get_icon(icon)
                except:
                    pass
                applications.remove(app)

            threading.Thread(target=g_icon).start()
    while applications:
        pass

def convert(d):
    if isinstance(d, dict):
        try:
            d = json.dumps(d, indent=4)
        except TypeError:
            pass
    return str(d)


def debug_data(*args, **kwargs):
    data = []
    for arg in args:
        data += [convert(arg)]

    for key, value in kwargs.items():
        data += [key + ': ' + convert(value)]
    return '\n'.join(data)


class _LOGGER(object):
    file_writer = None

    @classmethod
    def error(cls, *args, **kwargs):

        if 'err' in kwargs:
            err = kwargs.pop('err')
        else:
            err = traceback.format_exc()

        if cls.file_writer:
            cls.file_writer.write(
                '%s.%s: %s\n' % (__name__, err, debug_data(*args, **kwargs))
            )

    @classmethod
    def debug(cls, direction, *args, **kwargs):

        if cls.file_writer:
            cls.file_writer.write(
                '%s: DEBUG: %s  %s\n' %
                (__name__, direction, debug_data(*args, **kwargs))
            )


class SonyAPIError(Exception):

    def __init__(self, msg):
        if isinstance(msg, dict):
            msg = json.dumps(msg, indent=4)

        _LOGGER.error(self.__class__.__name__, msg)
        self.msg = msg

    def __str__(self):
        return self.msg


class PinError(SonyAPIError):
    pass


class RegisterTimeoutError(SonyAPIError):
    pass


class NotImplementedError(SonyAPIError):
    # 501,"Not Implemented"
    pass


class UnsupportedError(SonyAPIError):
    # 15, "unsupported"
    pass


class JSONRequestError(SonyAPIError):
    # 7, "Illegal State"
    # 7, "Clock is not set"
    # 12, "getLEDIndicatorStatus"

    def __init__(self, num, msg):
        self._num = num
        self._msg = msg

    def __str__(self):
        return 'error: %d, %s' % (self._num, self._msg)

    def __eq__(self, other):
        return other in (self._num, self._msg)


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

class IPAddressError(SonyAPIError):
    pass


class SonyAPI(object):
    PinError = PinError
    RegisterTimeoutError = RegisterTimeoutError
    JSONRequestError = JSONRequestError
    CommandError = CommandError
    VolumeDeviceError = VolumeDeviceError
    RegisterError = RegisterError
    IRCCError = IRCCError
    SendError = SendError
    IPAddressError = IPAddressError
    UnsupportedError = UnsupportedError
    NotImplementedError = NotImplementedError

    def __init__(self, ip_address=None, mac=None, pin=0000, psk=None, debug=None):
        _LOGGER.file_writer = debug

        self._ircc_url = 'http://%s/sony/IRCC' % ip_address
        self._access_url = 'http://%s/sony/accessControl' % ip_address

        if ip_address is None:
            ip_addresses = SonyAPI.discover()

            display_addresses = []
            for display_ip in ip_addresses:
                display_mac = _get_mac_address(display_ip)
                if display_mac == mac:
                    self._ip_address = display_ip
                    break
                display_addresses += [display_ip, display_mac]
            else:
                display_addresses = []

            if display_addresses:
                address_text = '\n'.join(
                    '%d: %s - %s' % (i, address[0], address[1])
                    for i, address in enumerate(display_addresses)
                )
                address_text += (
                    '\n\n Please input the number for '
                    'the TV you want to control\n'
                )
                index = int(raw_input(address_text))
                self._ip_address = display_addresses[index][0]
        else:
            self._ip_address = ip_address

        if not self._ip_address:
            raise IPAddressError('')

        self.icon_cache = {}

        self._volume = None
        self._channel = 0
        self._cookies = None
        self._event_threads = []
        self._pin_timer = None
        self._timeout_event = None
        self._guid = '24F26C67-5A50-4B08-8754-80EBAF880379'
        self.media = None
        self._psk = psk
        self._icon_thread = threading.Thread(target=cache_icons, args=(self,))
        if psk:
            self._pin = pin
        else:
            self._pin = None
            self.pin = pin

    def run_tests(self):
        import test
        test.run(self)

    @property
    def pin(self):
        return self._pin

    @pin.setter
    def pin(self, pin):
        nickname = socket.gethostbyaddr(
            socket.gethostname()
        )[0].replace('-', '')

        client_id = nickname + ':' + self._guid
        _LOGGER.debug('||', client_id=client_id)

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

        try:
            response = requests.post(
                self._access_url,
                data=authorization,
                headers=headers
            )
            response.raise_for_status()
            json_data = response.json()
            _LOGGER.debug('>>', json_data)

            if json_data:
                err = json_data.get('error')
                if err:
                    _LOGGER.error(json_data, err='JSONRequestError')
                    raise SonyAPI.JSONRequestError(*err)

            self._cookies = response.cookies
            self._pin = pin

        except requests.exceptions.HTTPError as exception_instance:
            if '401' in str(exception_instance):
                if pin:
                    _LOGGER.error(traceback.format_exc(), err='PinError')
                    raise SonyAPI.PinError(
                        'This device is not registered or the PIN is '
                        'invalid.\n\n' +
                        traceback.format_exc()
                    )
                else:
                    timed_out = False
                    self._timeout_event = threading.Event()

                    def register_timeout():
                        global timed_out
                        self._timeout_event.wait(60000)

                        if not self._timeout_event.isSet():
                            timed_out = True
                            _LOGGER.error(err='RegisterTimeoutError')
                            raise SonyAPI.RegisterTimeoutError(
                                'Registration time has expired'
                            )

                    threading.Thread(target=register_timeout)

                    self._pin_timer = threading.Thread(target=register_timeout)
                    self._pin_timer.start()
                    pin = raw_input('Enter the pin that is seen on the TV')

                    if pin and not timed_out:
                        self.pin = pin
            else:
                _LOGGER.error(traceback.format_exc(), err='RegisterError')
                raise SonyAPI.RegisterError(
                    'Unknown HTTP Error: ' + traceback.format_exc()
                )

        except requests.exceptions.RequestException:
            _LOGGER.error(traceback.format_exc(), err='RegisterError')
            raise SonyAPI.RegisterError(
                'Unknown Request Error: ' + traceback.format_exc()
            )

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
        try:
            response = requests.post(
                self._ircc_url,
                headers=HEADER,
                cookies=self._cookies,
                data=(BODY % code).encode('UTF-8')
            )
            content = response.content
            _LOGGER.debug('>>', content)
            return content

        except requests.exceptions.RequestException:
            raise SonyAPI.IRCCError(traceback.format_exc())

    def send(self, url, method, return_index=0, **params):
        if not params:
            params = []
        else:
            params = [params]

        json_data = json.dumps(
            {'method': method, 'params': params, 'id': 1, 'version': '1.0'}
        )
        _LOGGER.debug('||', json_data=json_data)

        try:
            if self._psk is None:
                header = dict(cookies=self._cookies)
            else:
                header = dict(headers={'X-Auth-PSK': self._psk})

            header['data'] = json_data.encode('UTF-8')

            _LOGGER.debug('||', header=header)
            url = 'http://%s/sony/%s' % (self._ip_address, url)
            _LOGGER.debug('<<', url=url, header=header)
            response = requests.post(url, **header)
            response = json.loads(response.content.decode('utf-8'))
            _LOGGER.debug('>>', response=response)

            err = response.get('error')

            if err:
                err_num, err_msg = err
                if err_num == 501:
                    _LOGGER.error(err, err='NotImplementedError')
                    raise NotImplementedError(err_msg)

                elif err_num == 15:
                    _LOGGER.error(err, err='UnsupportedError')
                    raise UnsupportedError(err_msg)
                else:
                    _LOGGER.error(err, err='JSONRequestError')
                    raise SonyAPI.JSONRequestError(err_num, err_msg)

            if isinstance(response['result'], list):
                return response['result'][return_index]
            else:
                return response['result']

        except requests.exceptions.RequestException:
            _LOGGER.error(traceback.format_exc(), err='SendError')
            raise SonyAPI.SendError(traceback.format_exc())

    def cache_icons(self):
        if self._icon_thread is not None and not self._icon_thread.isAlive():
            self._icon_thread.start()

    @property
    def volume(self):
        if self._volume is None:
            self._volume = volume.Volume(self)
        return self._volume

    @volume.setter
    def volume(self, value):
        self.volume.speaker += int(value)

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

    def mhl_power_feed_mode(self, enabled):
        self.send('cec', 'setMhlPowerFeedMode', enabled=enabled)

    mhl_power_feed_mode = property(fset=mhl_power_feed_mode)

    def mhl_auto_input_change_mode(self, enabled):
        self.send('cec', 'setMhlAutoInputChangeMode', enabled=enabled)

    mhl_auto_input_change_mode = property(fset=mhl_auto_input_change_mode)

    def cec_control_mode(self, enabled):
        self.send('cec', 'setCecControlMode', enabled=enabled)

    cec_control_mode = property(fset=cec_control_mode)

    def cec_power_sync_mode(self, (on_sync, off_sync)):
        self.send(
            'cec',
            'setPowerSyncMode',
            sourcePowerOnSync=on_sync,
            sinkPowerOffSync=off_sync
        )

    cec_power_sync_mode = property(fset=cec_power_sync_mode)

    @property
    def speaker_settings(self):
        settings = {}

        try:
            results = self.send('audio', 'getSpeakerSettings')
            for result in results:
                settings[result['target']] = result['currentValue']
        except:
            pass

        return speaker.Settings(self, **settings)

    @property
    def _date_time_format(self):
        return self.send('system', 'getDateTimeFormat')

    @property
    def time_format(self):
        return self._date_time_format['timeFormat']

    @property
    def date_format(self):
        return self._date_time_format['dateFormat']

    @property
    def time(self):
        try:
            t = self.send('system', 'getCurrentTime')
            version = self.send('system', 'getVersions')[-1]

            if version == '1.0':
                return t

            if version == '1.1':
                return t['dateTime']
        except JSONRequestError as err:
            if err == 'Clock is not set':
                return None
            else:
                raise

    @time.setter
    def time(self, date_time=datetime.now()):
        self.send(
            'system',
            'setCurrentTime',
            dateTime=date_time.strftime('%Y-%M-%DT%H:%M:%S%z')
        )

    @property
    def postal_code(self):
        try:
            return self.send('system', 'getPostalCode')['postalCode']
        except UnsupportedError:
            return None

    @postal_code.setter
    def postal_code(self, code):
        self.send('system', 'setPostalCode', postalCode=code)

    @property
    def power_saving_mode(self):
        mode = self.send('system', 'getPowerSavingMode')['mode']

        if mode == 'off':
            return False
        else:
            return mode

    @power_saving_mode.setter
    def power_saving_mode(self, mode):
        if mode is False:
            mode = 'off'
        if mode is True:
            mode = 'on'

        self.send('system', 'setPowerSavingMode', mode=mode)

    @property
    def _interface_information(self):
        return self.send('system', 'getInterfaceInformation')

    @property
    def interface_server_name(self):
        return self._interface_information['serverName']

    @property
    def interface_model_name(self):
        return self._interface_information['modelName']

    @property
    def interface_product_name(self):
        return self._interface_information['productName']

    @property
    def interface_product_category(self):
        return self._interface_information['productCategory']

    @property
    def interface_version(self):
        return self._interface_information['interfaceVersion']

    @property
    def remote_model(self):
        return self.send('system', 'getRemoteControllerInfo')['type']

    @property
    def _system_information(self):
        return self.send('system', 'getSystemInformation')

    @property
    def product(self):
        return self._system_information['product']

    @property
    def mac(self):
        return self._system_information['macAddr']

    @property
    def name(self):
        return self._system_information['name']

    @property
    def language(self):
        return self._system_information['language']

    @language.setter
    def language(self, lang):
        self.send('system', 'setLanguage', language=lang)

    @property
    def cid(self):
        return self._system_information['language']

    @property
    def generation(self):
        return self._system_information['generation']

    @property
    def region(self):
        return self._system_information['region']

    @property
    def area(self):
        return self._system_information['area']

    @property
    def model(self):
        return self._system_information['model']

    @property
    def serial(self):
        return self._system_information['serial']

    @property
    def wol_mode(self):
        return self.send('system', 'getWolMode')['enabled']

    @wol_mode.setter
    def wol_mode(self, enabled):
        self.send('system', 'setWolMode', enabled=enabled)

    @property
    def color_keys_layout(self):
        return self.send('system', 'getColorKeysLayout')['colorKeysLayout']

    @property
    def led_indicator_status(self):
        try:
            return self.send('system', 'getLEDIndicatorStatus')
        except JSONRequestError as err:
            if err == 'getLEDIndicatorStatus':
                return None
            else:
                raise

    @led_indicator_status.setter
    def led_indicator_status(self, (status, mode)):
        self.send(
            'system',
            'setLEDIndicatorStatus',
            status=status,
            mode=mode
        )

    @property
    def remote_device_settings(self):
        # return list(
        #   dict(
        #       target=str,
        #       currentValue=str,
        #       deviceUIInfo":"string",
        #       title=str,
        #       titleTextID=str,
        #       type=str,
        #       isAvailable=bool,
        #       candidate=GeneralSettingsCandidate[]
        #   )
        # )

        try:
            return self.send('system', 'getRemoteDeviceSettings')
        except JSONRequestError as err:
            if err == 'getRemoteDeviceSettings':
                return None
            else:
                raise

    @property
    def _network_settings(self):
        # have to get the network interface name from the TV
        try:
            return self.send('system', 'getNetworkSettings')
        except JSONRequestError as err:
            if err == 'getNetworkSettings':
                return dict(
                    netif=None,
                    ipAddrV4=None,
                    ipAddrV6=None,
                    netmask=None,
                    hwAddr=None,
                    dns=None,
                    gateway=None
                )
            else:
                raise

    @property
    def network_ipv4(self):
        return self._network_settings['ipAddrV4']

    @property
    def network_netif(self):
        return self._network_settings['netif']

    @property
    def network_ipv6(self):
        return self._network_settings['ipAddrV6']

    @property
    def network_subnet_mask(self):
        return self._network_settings['netmask']

    @property
    def network_dns(self):
        return self._network_settings['dns']

    @property
    def network_mac(self):
        return self._network_settings['hwAddr']

    @property
    def network_gateway(self):
        return self._network_settings['gateway']

    @property
    def _system_supported_function(self):
        return self.send('system', 'getSystemSupportedFunction')

    @property
    def wol_mac(self):
        for option in self._system_supported_function:
            if option['option'] == 'WOL':
                return option['value']

    @property
    def chinese_software_keyboard_supported(self):
        for option in self._system_supported_function:
            if option['option'] == 'SupportedChineseSoftwareKeyboard':
                if option['value'] != 'no':
                    return True

        return False

    @property
    def banner_mode(self):
        return self.send('videoScreen', 'getBannerMode')

    @banner_mode.setter
    def banner_mode(self, value):
        self.send('videoScreen', 'setBannerMode', value=value)

    @property
    def scene_setting(self):
        return self.send('videoScreen', 'getSceneSetting')

    @scene_setting.setter
    def scene_setting(self, value):
        self.send('videoScreen', 'setSceneSetting', value=value)

    @property
    def pip_sub_screen_position(self):
        return self.send('videoScreen', 'getPipSubScreenPosition')['position']

    @pip_sub_screen_position.setter
    def pip_sub_screen_position(self, position):
        self.send('videoScreen', 'setPipSubScreenPosition', position=position)

    @property
    def audio_source_screen(self):
        return self.send('videoScreen', 'getAudioSourceScreen')['screen']

    @audio_source_screen.setter
    def audio_source_screen(self, screen):
        self.send('videoScreen', 'setAudioSourceScreen', screen=screen)

    def pap_screen_size(self, (screen, size)):
        self.send('videoScreen', 'setPapScreenSize', screen=screen, size=size)

    pap_screen_size = property(fset=pap_screen_size)

    @property
    def multi_screen_mode(self):
        return self.send('videoScreen', 'getMultiScreenMode')['mode']

    @multi_screen_mode.setter
    def multi_screen_mode(self, mode):
        self.send('videoScreen', 'setMultiScreenMode', mode=mode)
        #     option=dict(internetTVMode=self.multi_screen_internet_mode)
        # )

    @property
    def multi_screen_internet_mode(self):
        return self.send(
            'videoScreen',
            'getMultiScreenMode'
        )['option']['internetTVMode']

    @multi_screen_internet_mode.setter
    def multi_screen_internet_mode(self, mode):
        self.send(
            'videoScreen',
            'setMultiScreenMode',
            # mode=self.multi_screen_mode,
            option=dict(internetTVMode=mode)
        )

    @property
    def _parental_rating_settings(self):
        default = dict(
            ratingCountry=None,
            unratedLock=None,
            ratingTypeAge=None,
            ratingTypeSony=None,
            ratingCustomTypeTV=None,
            ratingCustomTypeMpaa=None,
            ratingCustomTypeCaFrench=None,
            ratingCustomTypeCaEnglish=None
        )
        default.update(**self.send('avContent', 'getParentalRatingSettings'))
        return default

    @property
    def parental_rating_setting_country(self):
        return self._parental_rating_settings['ratingCountry']

    @property
    def parental_rating_setting_unrated(self):
        return self._parental_rating_settings['unratedLock']

    @property
    def parental_rating_setting_age(self):
        return self._parental_rating_settings['ratingTypeAge']

    @property
    def parental_rating_setting_sony(self):
        return self._parental_rating_settings['ratingTypeSony']

    @property
    def parental_rating_setting_tv(self):
        return self._parental_rating_settings['ratingCustomTypeTV']

    @property
    def parental_rating_setting_mpaa(self):
        return self._parental_rating_settings['ratingCustomTypeMpaa']

    @property
    def parental_rating_setting_french(self):
        return self._parental_rating_settings['ratingCustomTypeCaFrench']

    @property
    def parental_rating_setting_english(self):
        return self._parental_rating_settings['ratingCustomTypeCaEnglish']

    @property
    def now_playing(self):
        res = self.send('avContent', 'getPlayingContentInfo')
        if res:
            return media.NowPlaying(self, **res)
        else:
            return media.NowPlaying(self)

    @property
    def scheme_list(self):
        schemes = self.send('avContent', 'getSchemeList')
        for scheme in schemes:
            yield scheme['scheme']

    @property
    def source_list(self):
        for scheme in self.scheme_list:
            sources = self.send('avContent', 'getSourceList', scheme=scheme)
            for source in sources:
                yield inputs.InputItem(self, **source)

    @property
    def content_count(self):
        for source in self.source_list:
            try:
                count = self.send(
                    'avContent',
                    'getContentCount',
                    source=source.uri
                )['count']
                yield (source, count)
            except JSONRequestError:
                continue

    def favorite_content_list(self, source=None, contents=('',)):
        if source is None:
            source = ''
        elif isinstance(source, inputs.InputItem):
            source = source.uri

        self.send(
            'avContent',
            'setFavoriteContentList',
            favSource=source,
            contents=list(contents)
        )

    @property
    def application_status_list(self):
        statuses = self.send('appControl', 'getApplicationStatusList')
        for status in statuses:
            yield (status['name'], status['status'])

    @property
    def application_list(self):
        applications = self.send('appControl', 'getApplicationList')
        for app in applications:
            yield application.Application(self, **app)

    def terminate_applications(self):
        self.send('appControl', 'terminateApps')

    @property
    def application_text_form(self):
        # 1.0
        #   command: self.send('appControl', 'getTextForm')
        #   results: [str]
        # 1.1
        #   command: self.send(
        # 'appControl',
        #  'getTextForm',
        #  encKey=str
        # )
        #   results: [str]
        import __builtin__
        raise __builtin__.NotImplementedError

    @application_text_form.setter
    def application_text_form(self, _):
        # 1.0
        #   command: self.send(
        # 'appControl',
        #  'setTextForm',
        # 1)
        #   results: [int]
        # 1.1
        #   command: self.send(
        # 'appControl',
        # 'setTextForm',
        #  text=str,
        #  encKey=str
        # )
        #   results: []
        import __builtin__
        raise __builtin__.NotImplementedError

    def application_csx_account(self, _):
        # 1.0
        #   command: self.send(
        # 'appControl',
        # 'setCsxUserAccount',
        # userName=str,
        # encKey=str,
        #  userID=str,
        # accessToken=str
        # )
        #   results: []
        import __builtin__
        raise __builtin__.NotImplementedError

    application_csx_account = property(fset=application_csx_account)

    @property
    def browser_text_url(self):
        try:
            result = self.send('browser', 'getTextUrl')
            if result:
                return browser.UrlItem(self, **result)
        except JSONRequestError as err:
            if err == 'Illegal State':
                return browser.UrlItem(self)
            else:
                raise

    @browser_text_url.setter
    def browser_text_url(self, browser_item=None, url=None):
        if url is not None:
            self.send('browser', 'setTextUrl', url=url)
        else:
            self.send('browser', 'setTextUrl', url=browser_item.url)

    @property
    def browser_bookmark_list(self):
        result = self.send('browser', 'getBrowserBookmarkList')
        for item in result:
            yield browser.BookmarkItem(self, **item)

    def act_browser_control(self):
        self.send('browser', 'actBrowserControl')

    @property
    def recording_status(self):
        return self.send('recording', 'getRecordingStatus')['status']

    @property
    def recording_supported_repeat_type(self):
        return self.send('recording', 'getSupportedRepeatType')

    @property
    def recording_history_list(self):
        results = self.send('recording', 'getHistoryList')
        results = list(
            recording.HistoryItem(**result)
            for result in results
        )

        return results

    @property
    def recording_schedule_list(self):

        results = self.send('recording', 'getScheduleList')
        return list(
            recording.ScheduleItem(self, **result)
            for result in results
        )

    @property
    def recording_conflict_list(self):
        return list(
            item for item in self.recording_schedule_list
            if item.overlap_status
        )

    @property
    def content_list(self):
        results = []
        sources = list(self.source_list)

        lock = threading.Lock()
        lock.acquire()

        while sources:
            def get(s, s_num):

                try:
                    content_list = self.send(
                        'avContent',
                        'getContentList',
                        source=s.uri
                    )
                    for content in content_list:
                        content['source'] = s
                        results.append(media.ContentItem(self, **content))
                except JSONRequestError:
                    pass

                if s_num == 1:
                    lock.release()

            threading.Thread(
                target=get,
                args=(sources.pop(0), len(sources))
            ).start()

        lock.acquire()

        return results

    @property
    def command_list(self):
        return list(self._command_list.keys())

    @property
    def _command_list(self):
        result = self.send('system', 'getRemoteControllerInfo', return_index=1)

        return dict(list(
            (command['name'], command['value'])
            for command in result
        ))

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

    @property
    def source(self):
        return self.now_playing.source

    @source.setter
    def source(self, source):
        if isinstance(source, inputs.InputItem):
            source.set()
        else:
            for inpt in self.source_list:
                if (
                    inpt.title == source or
                    inpt.uri == source or
                    source.lower() in inpt.uri
                ):
                    inpt.set()

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

    @staticmethod
    def discover(timeout=30):

        start_time = time.time()
        found_addresses = []
        while time.time() - start_time < timeout:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                sock.settimeout(5.0)
                dest = socket.gethostbyname(SSDP_ADDR)
                sock.sendto(SSDP_REQUEST, (dest, SSDP_PORT))
                sock.settimeout(5.0)
                data = sock.recv(1000)
                sock.close()
            except socket.timeout:
                try:
                    sock.close()
                    continue
                except socket.error:
                    continue

            response = data.decode('utf-8')
            match = re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", response)
            if match:
                found_addresses += [match.group()]

        return found_addresses

    def register_event_callback(self, callback):
        if self._event_threads:
            for thread in self._event_threads:
                thread.add_callback(callback)
        else:
            rendering = EventSocketThread(
                'RenderingControl',
                self._ip_address,
                8000
            )
            av = EventSocketThread(
                'AvTransport',
                self._ip_address,
                8001
            )
            connection = EventSocketThread(
                'ConnectionManager',
                self._ip_address,
                8002
            )
            ircc = EventSocketThread(
                'IRCC',
                self._ip_address,
                8003
            )

            rendering.add_callback(callback)
            av.add_callback(callback)
            connection.add_callback(callback)
            ircc.add_callback(callback)

            rendering.start()
            av.start()
            connection.start()
            ircc.start()
            self._event_threads = [rendering, av, connection, ircc]
            return callback

    def unregister_event_callback(self, callback):
        for thread in self._event_threads[:]:
            thread.remove_callback(callback)
            if not thread.callback_count():
                thread.stop()
                self._event_threads.remove(thread)


class EventSocketThread(object):

    def __init__(self, service, ip, local_port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        self.local_ip_address = s.getsockname()[0]
        self.local_port = local_port
        self.service = service
        self.url = 'http://%s:52323/upnp/event/%s' % (ip, service)
        self.header = dict(
            NT='upnp:event',
            CALLBACK='<http://%s:%d/>' % (self.local_ip_address, local_port),
            TIMEOUT='Second-1800'
        )
        self.sid = None
        self.sock = None
        self._callbacks = []
        self._listen_event = threading.Event()
        self._listen_thread = threading.Thread(target=self.listen)

    def add_callback(self, callback):
        if callback not in self._callbacks:
            self._callbacks += [callback]

    def remove_callback(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def callback_count(self):
        return len(self._callbacks)

    def listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1700)
        self.sock.bind((self.local_ip_address, self.local_port))

        while not self._listen_event.isSet():
            try:
                self.sock.listen(3)
                conn, address = self.sock.accept()
                data = conn.recv(4096)
                conn.close()
                print data
            except socket.timeout:
                header = dict(
                    SID=self.sid,
                    TIMEOUT='Second-1800'
                )
                requests.request(
                    'SUBSCRIBE',
                    self.url,
                    headers=header
                )

        header = dict(
            SID=self.sid
        )
        requests.request('UNSUBSCRIBE', self.url, headers=header)

    def start(self):
        response = requests.request(
            'SUBSCRIBE',
            self.url,
            headers=self.header
        )
        self.sid = response.headers['SID']
        self._listen_thread.start()

    def stop(self):
        self._listen_event.set()
        self.sock.shutdown(socket.SHUT_RDWR)
        self._listen_thread.join(3.0)
