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
import json
import socket
import struct
import requests
import traceback
import application
import volume
import media
import recording
import browser
import inputs
import channel
from datetime import datetime
from utils import get_icon

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


def cache_icons(sony_api):
    applications = sony_api.send('appControl', 'getApplicationList')
    for app in applications:
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
            threading.Thread(target=g_icon).start()

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


class SonyAPI(object):
    PinError = PinError
    RegisterTimeoutError = RegisterTimeoutError
    JSONRequestError = JSONRequestError
    CommandError = CommandError
    VolumeDeviceError = VolumeDeviceError
    RegisterError = RegisterError
    IRCCError = IRCCError
    SendError = SendError

    channel = channel.Channel()

    def __init__(self, ip_address, pin=0000, psk=None, debug=None):
        _LOGGER.file_writer = debug

        self._ircc_url = 'http://%s/sony/IRCC' % ip_address
        self._access_url = 'http://%s/sony/accessControl' % ip_address
        self._ip_address = ip_address
        self.icon_cache = {}
        self._thread = None
        self._thread_event = threading.Event()
        self._callbacks = []
        self._volume = None
        self._cookies = None
        self._commands = []
        self._content_mapping = []
        self._pin_timer = None
        self._timeout_event = None
        self._guid = '24F26C67-5A50-4B08-8754-80EBAF880379'
        self.media = None
        self._psk = psk
        self._icon_thread = threading.Thread(target=cache_icons, args=(self,))
        if psk:
            self._pin = pin
            self._icon_thread.start()
        else:
            self._pin = None
            self.pin = pin

    @property
    def pin(self):
        return self._pin

    @pin.setter
    def pin(self, pin):
        nickname = socket.gethostbyaddr(socket.gethostname())[0].replace('-', '')
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
        _LOGGER.debug('<<', access_url=self._access_url, authorization=authorization, headers=headers)

        try:
            response = requests.post(
                self._access_url,
                data=authorization,
                headers=headers
            )
            response.raise_for_status()
            json_data = response.json()
            _LOGGER.debug('>>', json_data)

            if json_data and json_data.get('error'):
                _LOGGER.error(json_data, err='JSONRequestError')
                raise SonyAPI.JSONRequestError(json_data)

            self._cookies = response.cookies
            self._pin = pin
            self._icon_thread.start()

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
        """
        "error": [7, "Illegal State"]
        "error": [7, "Clock is not set"]
        "error": [15, "unsupported"]
        "error": [12, "getLEDIndicatorStatus"]
        "error":[501,"Not Implemented"]
        """

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

            if response.get('error'):
                _LOGGER.error(response, err='JSONRequestError')
                raise SonyAPI.JSONRequestError(response)
            if isinstance(response['result'], list):
                return response['result'][return_index]
            else:
                return response['result']

        except requests.exceptions.RequestException:
            _LOGGER.error(traceback.format_exc(), err='SendError')
            raise SonyAPI.SendError(traceback.format_exc())

    @property
    def volume(self):
        if self._volume is None:
            self._volume = volume.Volume(self)
        return self._volume

    @volume.setter
    def volume(self, value):
        self.volume.speaker = value

    def reboot(self):
        self.send('guide', 'requestReboot')

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
        t = self.send('system', 'getCurrentTime')
        version = self.send('system', 'getVersions')[-1]

        if version == '1.0':
            return t

        if version == '1.1':
            return t['dateTime']

    @time.setter
    def time(self, date_time=datetime.now()):
        self.send(
            'system',
            'setCurrentTime',
            dateTime=date_time.strftime('%Y-%M-%DT%H:%M:%S%z')
        )

    @property
    def postal_code(self):
        return self.send(
            'system',
            'getPostalCode'
        )['postalCode']

    @postal_code.setter
    def postal_code(self, code):
        self.send('system', 'setPostalCode', postalCode=code)

    @property
    def power_saving_mode(self):
        mode = self.send(
            'system',
            'getPowerSavingMode'
        )['mode']

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
        return self.send(
            'system',
            'getRemoteControllerInfo'
        )['type']

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
        return self.send(
            'system',
            'getColorKeysLayout'
        )['colorKeysLayout']

    @property
    def led_indicator_status(self):
        return self.send(
            'guide',
            'getLEDIndicatorStatus'
        )

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
        return self.send(
            'guide',
            'getRemoteDeviceSettings',
            target=''
        )

    @property
    def _network_settings(self):
        return self.send(
            'system',
            'getNetworkSettings',
            netif=''
        )

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
        return self.send(
            'system',
            'getSystemSupportedFunction'
        )

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
    def pip_sub_screen_position(self):
        return self.send(
            'videoScreen',
            'getPipSubScreenPosition'
        )['position']

    @pip_sub_screen_position.setter
    def pip_sub_screen_position(self, position):
        self.send(
            'videoScreen',
            'setPipSubScreenPosition',
            position=position
        )

    @property
    def audio_source_screen(self):
        return self.send(
            'videoScreen',
            'getAudioSourceScreen'
        )['screen']

    @audio_source_screen.setter
    def audio_source_screen(self, screen):
        self.send('videoScreen', 'setAudioSourceScreen', screen=screen)

    def pap_screen_size(self, (screen, size)):
        self.send(
            'videoScreen',
            'setPapScreenSize',
            screen=screen,
            size=size
        )

    pap_screen_size = property(fset=pap_screen_size)

    @property
    def multi_screen_mode(self):
         return self.send(
            'videoScreen',
            'getMultiScreenMode'
        )['mode']

    @multi_screen_mode.setter
    def multi_screen_mode(self, mode):
        self.send(
            'videoScreen',
            'setMultiScreenMode',
            mode=mode,
            option=dict(internetTVMode=self.multi_screen_internet_mode)
        )

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
            mode=self.multi_screen_mode,
            option=dict(internetTVMode=mode)
        )

    @property
    def _parental_rating_settings(self):
        return self.send(
            'avContent',
            'getParentalRatingSettings'
        )

    @property
    def parental_rating_setting_country(self):
        ratings = self._parental_rating_settings
        if 'ratingCountry' in ratings:
            return ratings['ratingCountry']

    @property
    def parental_rating_setting_unrated(self):
        ratings = self._parental_rating_settings
        if 'unratedLock' in ratings:
            return ratings['unratedLock']

    @property
    def parental_rating_setting_age(self):
        ratings = self._parental_rating_settings
        if 'ratingTypeAge' in ratings:
            return ratings['ratingTypeAge']

    @property
    def parental_rating_setting_sony(self):
        ratings = self._parental_rating_settings
        if 'ratingTypeSony' in ratings:
            return ratings['ratingTypeSony']

    @property
    def parental_rating_setting_tv(self):
        ratings = self._parental_rating_settings
        if 'ratingCustomTypeTV' in ratings:
            return ratings['ratingCustomTypeTV']

    @property
    def parental_rating_setting_mpaa(self):
        ratings = self._parental_rating_settings
        if 'ratingCustomTypeMpaa' in ratings:
            return ratings['ratingCustomTypeMpaa']

    @property
    def parental_rating_setting_french(self):
        ratings = self._parental_rating_settings
        if 'ratingCustomTypeCaFrench' in ratings:
            return ratings['ratingCustomTypeCaFrench']

    @property
    def parental_rating_setting_english(self):
        ratings = self._parental_rating_settings
        if 'ratingCustomTypeCaEnglish' in ratings:
            return ratings['ratingCustomTypeCaEnglish']

    @property
    def scheme_list(self):
        schemes = self.send('avContent', 'getSchemeList')
        for scheme in schemes:
            yield scheme['scheme']

    @property
    def source_list(self):
        for scheme in self.scheme_list:
            sources = self.send(
                'avContent',
                'getSourceList',
                scheme=scheme
            )
            for source in sources:
                yield inputs.InputItem(self, **source)

    @property
    def playing_content(self):
        res = self.send(
            'avContent',
            'getPlayingContentInfo'
        )
        if len(res):
            return media.NowPlaying(self, **res)

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
        raise NotImplementedError

    @application_text_form.setter
    def application_text_form(self, params):
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
        raise NotImplementedError

    def application_csx_account(self, params):
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
        raise NotImplementedError

    application_csx_account = property(fset=application_csx_account)

    @property
    def browser_text_url(self):
        result = self.send('browser', 'getTextUrl')
        if len(result):
            return browser.UrlItem(self, **result[0])

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

    def act_browser_control(self, control):
        # 1.0
        #   command: self.send(
        # 'browser',
        #  'actBrowserControl',
        #  control=str
        # )
        #   results: [int]
        raise NotImplementedError

    @property
    def recording_status(self):
        return self.send(
            'recording',
            'getRecordingStatus'
        )['status']

    @property
    def recording_supported_repeat_type(self):
        return self.send(
            'recording',
            'getSupportedRepeatType'
        )[0]

    @property
    def recording_history_list(self):
        results = self.send(
            'recording',
            'getHistoryList',
        )
        results = list(
            recording.HistoryItem(**result)
            for result in results
        )

        return results

    @property
    def recording_schedule_list(self):

        results = self.send(
            'recording',
            'getScheduleList'
        )
        results = list(
            recording.ScheduleItem(self, **result)
            for result in results
        )

        return results

    @property
    def recording_conflict_list(self):
        return (
            item for item in self.recording_schedule_list
            if item.overlap_status
        )

    @property
    def content_list(self):
        results = []
        sources = list(self.source_list)

        for source in sources[:]:
            def get(s):
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
                sources.remove(s)

            threading.Thread(target=get, args=(source,)).start()

        while sources:
            pass

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
        return self.playing_content.title

    @source.setter
    def source(self, source):
        for inpt in self.external_input_status:
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
                events += [MEDIA_EVENT]
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

    @staticmethod
    def discover():
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
        import time
        start_time = int(time.time())

        sock.setblocking(0)

        while (int(time.time()) - start_time) <= 30:
            try:
                data, address = sock.recvfrom(4096)
            except socket.error:
                pass
            else:
                data_dict = dict()
                for d in data.decode('utf-8').rstrip().split('\r\n')[1:]:
                    key, value = d.split(':', 1)
                    data_dict[key] = value
                result += [data_dict]
        return result
