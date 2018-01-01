# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.


from __future__ import absolute_import

from datetime import datetime
from .exception import UnsupportedError
from . import container

"""
notifyPowerStatus
notifySWUpdateInfo
"""


class System(object):

    def __init__(self, sony_api):
        self.__sony_api = sony_api
        self._interface_information = None
        self._system_information = None
        self._system_supported_function = None
        self._network_settings = None

    @property
    def network_settings(self):
        """
        Gets the network settings for the device.

        When this is called a system.NetworkSettings instance is returned. It
        gets constructed when the call is made, it only gets constructed once.
        This is so that if you are not using it at all it doesn't consume any
        system resources.

        :return: system.NetworkSettings instance
        :rtype: system.NetworkSettings
        """
        if self._network_settings is None:
            self._network_settings = NetworkSettings(self.__sony_api)
        return self._network_settings

    @property
    def interface_information(self):
        """
        Gets the api interface information for the device.

        When this is called a system.InterfaceInformation instance is returned.
        It gets constructed when the call is made, it only gets constructed
        once. This is so that if you are not using it at all it doesn't
        consume any system resources.

        :return: system.InterfaceInformation instance
        :rtype: system.InterfaceInformation
        """
        if self._interface_information is None:
            self._interface_information = InterfaceInformation(self.__sony_api)
        return self._interface_information

    @property
    def system_information(self):
        """
        Gets the system information for the device.

        When this is called a system.SystemInformation instance is returned.
        It gets constructed when the call is made, it only gets constructed
        once. This is so that if you are not using it at all it doesn't
        consume any system resources.

        :return: system.SystemInformation instance
        :rtype: system.SystemInformation
        """
        if self._system_information is None:
            self._system_information = SystemInformation(self.__sony_api)
        return self._system_information

    @property
    def system_supported_function(self):
        """
        Gets the system supported functions for the device.

        The system supported functions are mainly various GUI related settings.

        When this is called a system.SystemSupportedFunction instance is
        returned. It gets constructed when the call is made, it only gets
        constructed once. This is so that if you are not using it at all it
        doesn't consume any system resources.

        :return: system.SystemSupportedFunction instance
        :rtype: system.SystemSupportedFunction
        """
        if self._system_supported_function is None:
            self._system_supported_function = SystemSupportedFunction(
                self.__sony_api
            )
        return self._system_supported_function

    def __send(self, method, **params):
        return self.__sony_api.send('system', method, **params)

    @property
    def available_firmware_updates(self):
        """
        Checks to see if thee are available firmware updates.

        :return: container.Container instance that holds information about an
            available update.
        :rtype: container.Container
        """
        result = self.__send('getSWUpdateInfo', network=True)[0]['swInfo']
        return container.Container(**result)

    @property
    def sleep_timer(self):
        """
        Gets the sleep timer.

        :return: Possible values:
            120 - After 120 minutes.
            90 - After 90 minutes.
            80 - After 80 minutes.
            70 - After 70 minutes.
            60 - After 60 minutes.
            50 - After 50 minutes.
            40 - After 40 minutes.
            30 - After 30 minutes.
            20 - After 20 minutes.
            10 - After 10 minutes.
            0 - Do not automatically turn off.
        :rtype: int
        """
        result = self.__send(
                'getSleepTimerSettings',
                target='sleepTimerMin'
            )[0]['currentValue']

        if result == 'off':
            result = 0
        return int(result)

    @sleep_timer.setter
    def sleep_timer(self, value):
        """
        Sets the sleep timer.

        :param value: Allowed values:
            120 - After 120 minutes.
            90 - After 90 minutes.
            80 - After 80 minutes.
            70 - After 70 minutes.
            60 - After 60 minutes.
            50 - After 50 minutes.
            40 - After 40 minutes.
            30 - After 30 minutes.
            20 - After 20 minutes.
            10 - After 10 minutes.
            0 - Do not automatically turn off.
        :return: None:
        :rtype: None
        """
        if not value:
            value = 'off'

        self.__send(
            'setSleepTimerSettings',
            settings=[dict(target='sleepTimerMin', value=str(value))]
        )

    @property
    def time_format(self):
        """
        Gets device GUI time format.

        :return: GUI time format.
        :rtype: str
        """
        return self.__send('getDateTimeFormat')[0]['timeFormat']

    @property
    def date_format(self):
        """
        Gets device GUI date format.

        :return: GUI date format.
        :rtype: str
        """
        return self.__send('getDateTimeFormat')[0]['dateFormat']

    @property
    def postal_code(self):
        """
        Gets the device postal code.

        :return: Postal code.
        :rtype: str
        """
        return self.__send('getPostalCode')[0]['postalCode']

    @postal_code.setter
    def postal_code(self, value):
        """
        Sets the device postal code.

        :param value: Postal code.
        :type value: str

        :return: None
        :rtype: None
        """
        self.__send('setPostalCode', postalCode=value)

    @property
    def time(self):
        """
        Gets the current device time.

        :return: datetime.datetime instance
        :rtype: datetime.datetime
        """
        res = self.__send('getCurrentTime')[0]

        if isinstance(res, dict):
            date_time = res['datetime']
        else:
            date_time = res

        return datetime.strptime(date_time, '%Y-%M-%DT%H:%M:%S%z')

    @time.setter
    def time(self, value=datetime.now()):
        """
        Sets the device time.

        :param value: datetime.datetime instance
        :type value: datetime.datetime
        :return: None
        :rtype: None
        """
        self.__send(
            'setCurrentTime',
            dateTime=value.strftime('%Y-%M-%DT%H:%M:%S%z')
        )

    @property
    def color_keys_layout(self):
        """
        Gets color keys layout.

        :return: Color key layout information of remote controller.
            "B" - blue key
            "R" - red key
            "G" - green key
            "Y" - yellow key
            (ex) "BRGY"
            (ex) "RGYB"
        :rtype: str

        """
        return self.__send('getColorKeysLayout')[0]['colorKeysLayout']

    @property
    def power_saving_mode(self):
        """
        Gets the power saving mode.

        :return: Possible values:
            "off" - Power saving mode is disabled.
            "low" - Power saving mode is enabled with level low.
            "high" - Power saving mode is enabled with level high.
            "pictureOff" - Power saving mode is enabled with panel output off
        :rtype: str
        """
        return self.__send('getPowerSavingMode')[0]['mode']

    @power_saving_mode.setter
    def power_saving_mode(self, value):
        """
        Gets the power saving mode.

        :param value: Possible values:
            "off" - Power saving mode is disabled.
            "low" - Power saving mode is enabled with level low.
            "high" - Power saving mode is enabled with level high.
            "pictureOff" - Power saving mode is enabled with panel output off
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('setPowerSavingMode', mode=value)

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
        """
        No idea what this does.
        """
        return self.__send('getRemoteDeviceSettings')[0]

    def led_indicator_status(self, value):
        """
        Sets the LED indicator state.

        :param value: Possible values:
                True - "on", LED is enabled.
            False = "off", LED is disabled.
        :type value: bool

        :return: None
        :rtype: None
        """
        self.__send(
            'setLEDIndicatorStatus',
            status=value,
            mode="PictureFrame"
        )

    led_indicator_status = property(fset=led_indicator_status)


class SystemSupportedFunction(object):

    def __init__(self, sony_api):

        self.__sony_api = sony_api

    def __send(self, key):
        options = self.__sony_api.send(
            'system',
            'getSystemSupportedFunction'
        )[0]

        for option in options:
            if option['option'] == key:
                return option['value']
        raise UnsupportedError

    @property
    def front_panel_brightness(self):
        """
        Gets Front Panel Brightness.

        :return: Brightness of the system display:
            "bright" - Front panel brightness is bright.
            "dark"  - Front panel brightness is dark.
            "off" - Front panel brightness is off.
        :rtype: str
        """
        return self.__send('FrontPanelBrightness')

    @property
    def av_separation(self):
        """
        Gets AV Separation.

        :return: AV Separation Output Mode or not:
            True - "on", Output data in the AV Separation Output Mode.
            False - "off" , Output data in the Multi Output Mode.
        :rtype: bool
        """
        return self.__send('AVSeparation') == 'on'

    @property
    def auto_display(self):
        """
        Gets Auto Display.

        :return: Auto Display settings:
            True - "on", OSD is displayed automatically when state or mode etc.
            is changed.
            False - "off" , OSD is displayed only by user operation.
        :rtype: bool
        """
        return self.__send('AutoDisplay') == 'on'

    @property
    def screen_saver(self):
        """
        Gets Screen Saver Mode.
        :return: Screen Saver feature or not.
            True - "on", Enable Screen Saver.
            False - "off" , Disable Screen Saver.
        :rtype: bool
        """
        return self.__send('ScreenSaver') == 'on'

    @property
    def software_update_notification(self):
        """
        Gets Software Update Notification Mode.

        :return: Network update notification function:
            True - "on", Enable Network update notification function.
            False - "off", Disable Network update notification function.
        :rtype: bool
        """
        return self.__send('SoftwareUpdateNotification') == 'on'

    @property
    def rich_meta_information(self):
        """
        Gets Rich Meta Information (Gracenote) settings
        :return: Connecting to Gracenote.
            "auto" - When playback is stopped, BD ROM/DVD ROM creates TOC for
            Gracenote connection and obtains information from Gracenote.
            Whereas CD DA creates TOC and obtains information from Gracenote
            upon mounting.
            "manual" - Creates TOC and obtains information from Gracenote only
            when there is a request for information acquisition, such as
            window display.
        :rtype: str
        """
        return self.__send('RichMetaInformation')

    @property
    def auto_renderer(self):
        """
        Gets Auto Renderer.

        :return: Access permission setting value required when registering new
            DMC/+PU+, DMR and DMP.
            True - "on", When there is an access from new DMC/+PU+ (Send
            contents etc.), DMR and DMP registers Access Permission as "Allow"
            state. When it exceeds the max number of possible Access
            Permissions, is registers Access Permission as "Block(Hold)" state.
            False - "off", When there is an access from new DMC/+PU+ (Send
            contents etc.), DMR and DMP registers Access Permission as
            "Block(Hold)" state.
        :rtype: bool
        """
        return self.__send('AutoRenderer') == 'on'

    @property
    def name_of_device(self):
        """
        Gets the name of the device.

        :return: Name of a device.
            (ex) "BD Player in Living"
        :rtype: str
        """
        return self.__send('NameDevice')

    @property
    def ir_repeat(self):
        """
        Gets IR Repeat.

        :return: Whether a server receives and sends IR signal to other device.
            True - "on", A server receives and sends IR signal for other
            device.
            False - "off", A server does not receive and send IR signal to
            other device.
        :rtype: bool
        """
        return self.__send('IRRepeat') == 'on'

    @property
    def cis_ip_control(self):
        """
        Gets CIS-IP Control

        :return: Whether a dedicated controller (home automation
        controller) on the home network is allowed to control a device by
        CIS-IP control.
            True - "on", Enable CIS-IP control function
            False - "off", Disable CIS-IP control function
        :rtype: bool
        """
        return self.__send('CIS-IPControl') == 'on'

    @property
    def auto_update(self):
        """
        Gets Auto Update

        :return: Whether to enable auto software update function or not.
            True - "on", Enable Auto SW Update function
            False - "off" , Disable Auto SW Update function
        :rtype: bool
        """
        return self.__send('AutoUpdate') == 'on'

    @property
    def time_zone_settings(self):
        """
        Gets Time Zone settings.

        :return: Set Time Zone unique name (Area/Location) used in tz database
            or offset value is also able to be added by the following format.
            <Time Zone unique name used in tz database>|
            <optional offset value (minutes)>

            (ex) "America/New_York|-240"
            (ex) "Asia/Tokyo|540"
        :rtype: str
        """
        return self.__send('TimeZone')

    @property
    def osd_language(self):
        """
        Gets OSD Language.

        :return: OSD language code represented by BCP47 (RFC4646 and RFC4647)
            (ex) "ja"
            (ex) "en-US"
        :rtype: str
        """
        return self.__send('OSDLanguage')

    @property
    def client_language(self):
        """
        Gets Client Language.

        :return: Client language code represented by BCP47
            (RFC4646 and RFC4647)
            (ex) "ja"
            (ex) "en-US"
        :rtype:: str
        """
        return self.__send('ClientLanguage')

    @property
    def quick_start_mode(self):
        """
        Gets Quick Start Mode.

        :return: Whether to set Standby mode during Power Off or not.
            True - "on", Standby mode is set during Power Off.
            False - "off", Standby mode is not set during Power Off.
        :rtype: bool
        """
        return self.__send('QuickStart') == 'on'

    @property
    def auto_standby(self):
        """
        Gets Auto Standby.

        This device automatically changes to Power OFF, when judged that there
        is no operation for a certain period of time.

        :return:  Whether to Auto Standby feature or not.
            True - "on", Enable Auto Standby.
            False - "off", Disable Auto Standby.
        :rtype: bool
        """
        return self.__send('AutoStandby') == 'on'

    @property
    def network_standby_mode(self):
        """
        Gets Network standby mode.

        Whether to enable Network standby mode.

        :return: When a device is Network standby state, network is available
            even in power off state.
            True - "on", Enable Network standby mode.
            False - "off", Disable Network standby mode.
        :rtype: bool
        """
        return self.__send('NetworkStandby') == 'on'

    @property
    def secure_link_mode(self):
        """
        Gets Secure Link mode.

        :return: Secure Link to a specific surround amplifier in range of
            wireless reception.
            True - "on", Enable Secure Link function.
            False - "off", Disable Secure Link function.
        :rtype: bool
        """
        return self.__send('SecureLink') == 'on'

    @property
    def rf_band(self):
        """
        Gets RF Band.

        :return: RF Band which RF Channel belongs to.
            "auto" - Set the value of RF Band automatically.
            "5.2GHz" - Set 5.2GHz as RF Band.
            "5.8GHz" - Set 5.8GHz as RF Band.
        :rtype: str
        """
        return self.__send('RFBand')

    @property
    def rf_channel(self):
        """
        Gets RF Channel.

        :return: RF Channel.
            "auto" - Set the value of RF Channel automatically.
            1 - Set 1 channel as RF Channel.
            2 - Set 2 channel as RF Channel.
            3 - Set 3 channel as RF Channel.
        :rtype: int, str
        """
        return self.__send('RFChannel')

    @property
    def sleep_timer(self):
        """
        Gets Sleep Timer.

        :return: Sleep Timer (min) to turn off automatically at a specified
            time.
            120 - 120 min
            90 - 90 min
            80 - 80 min
            70 - 70 min
            60 - 60 min
            50 - 50 min
            40 - 40 min
            30 - 30 min
            20 - 20 min
            10 - 10 min
            0 - OFF
            None - Sleep Timer Settings is Unknown.
        :rtype: int, None
        """
        res = self.__send('SleepTimer')

        if res.isdigit():
            return int(res)
        if res == 'off':
            return 0
        return None

    @property
    def privacy_setting(self):
        """
        Gets Privacy Setting

        :return: Whether to enable Privacy setting or not.
            True - "on", Enable Privacy setting
            False - "off", Disable Privacy setting
        :rtype: bool
        """
        return self.__send('PrivacySetting') == 'on'

    @property
    def activate_status(self):
        """
        Gets Activate status.

        :return: Activate status of Cast for Audio.
            True - "on", Enable Activate status
            False - "off", Disable Activate status
        :rtype: bool
        """
        return self.__send('ActivateStatus') == 'on'

    @property
    def current_cast(self):
        """
        Gets Current Cast for Audio service version.

        :return: Current Cast for Audio service version information.
            (ex) "Ver.xxx"
        :rtype: str
        """
        return self.__send('CurrentCastforAudio')

    @property
    def remote_device_permission(self):
        """
        Gets Remote device permission setting.

        :return: Whether to permit access from remote device, which can access
            server device from outside the door.
            True - "on", access permitted.
            False - "off", access not permitted.
        :rtype: bool
        """
        return self.__send('RemoteDevicePermission') == 'on'

    @property
    def wol_mac(self):
        """
        Gets the MAC address for WOL.

        This is just in case the WOL is software set.

        :return: MAC Address
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('WOL')

    @property
    def chinese_software_keyboard_supported(self):
        """
        Gets if the device supports chinese software keyboard.

        :return: Possible values:
            True - Supports
            False - No support
        :rtype: bool
        :raises: UnsupportedError
        """
        if self.__send('SupportedChineseSoftwareKeyboard') == 'no':
            return False
        else:
            return True


class NetworkSettings(object):

    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, key):
        # have to get the network interface name from the TV

        res = self.__sony_api.send(
            'system',
            'getNetworkSettings',
            netif=''
        )[0][0]

        if key in res:
            return res[key]
        else:
            raise UnsupportedError

    @property
    def ipv4(self):
        """
        Gets the IP version 4 address.

        :return: IPV4 address.
        :rtype: str
        """
        return self.__send('ipAddrV4')

    @property
    def netif(self):
        """
        Gets the network interface name.

        :return: (ex) "eth0", "wlan0"
        :rtype: str
        """
        return self.__send('netif')

    @property
    def ipv6(self):
        """
        Gets the IP version 6 address.

        :return: IPV6 address.
        :rtype: str
        """
        return self.__send('ipAddrV6')

    @property
    def subnet_mask(self):
        """
        Gets the subnet mask.

        :return: Subnet mask.
        :rtype: str
        """
        return self.__send('netmask')

    @property
    def dns(self):
        """
        Gets the DNS servers.

        :return: List of DNS servers.
        :rtype: list
        """
        return self.__send('dns')

    @property
    def mac(self):
        """
        Gets the hardware address.

        :return: MAC address
        :rtype: str
        """
        return self.__send('hwAddr')

    @property
    def gateway(self):
        """
        Gets the default gateway address.

        :return: Gateway address.
        :rtype: str
        """
        return self.__send('gateway')

    @property
    def wol(self):
        """
        Gets the Wake On Lan (WOL) state.

        :return: Possible values:
            True - "on", WOL is enabled
            False - "off", WOL is disabled
        :rtype: bool
        """
        return self.__sony_api.send('system', 'getWolMode')[0]['enabled']

    @wol.setter
    def wol(self, value):
        """
        Gets the Wake On Lan (WOL) state.

        :param value: Possible values:
            True - "on", WOL is enabled
            False - "off", WOL is disabled
        :type value: bool

        :return: None
        :rtype: None
        """
        self.__sony_api.send('system', 'setWolMode', enabled=value)


class InterfaceInformation(object):

    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, key):
        res = self.__sony_api.send('system', 'getInterfaceInformation')[0]

        if key in res:
            return res[key]
        else:
            raise UnsupportedError

    @property
    def server_name(self):
        """
        Gets the server name.

        In case device can launch multiple Scalar WebAPI servers, return this
        server's name for client to distinguish.

        :return: Server name.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('serverName')

    @property
    def model_name(self):
        """
        Gets the model name

        :return: Model name.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('modelName')

    @property
    def product_name(self):
        """
        Gets more detailed product information.

        :return: Product information.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('productName')

    @property
    def product_category(self):
        """
        Gets Category name of device.

        :return: Possible values:
            "camera" - Cameras and Camcorders.
            "tv" - TV.
            "internetTV" - Internet player with Google TV.
            "videoServer" - The device that can serve downloadable video
            contents.
            "homeTheaterSystem" - Home theater system.
            "videoPlayer" - Video Player.
            "personalAudio" - Personal Audio product.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('productCategory')

    @property
    def version(self):
        """
        gets interface version.

        Version for client to change its behavior w.r.t significant difference
        within productCategory. This version is managed/controlled within each
        productCategory.

        :return: value is composed of "[X].[Y].[Z]", where [X], [Y] and [Z] are
            string representing integer and concatenated with period "." in
            between.

            [X] - This value is assigned and incremented so that client can
            distinguish any significant difference of device or group of
            devices within productCategory. How this value is assigned depends
            on each productCategory.
            [Y] - This value represents the version of API sets. This version
            must be incremented in case supported APIs are added or deleted.
            [Z] -  This value must be incremented in case any behavior of
            existing APIs are changed within [X.Y].
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('interfaceVersion')

    @property
    def remote_model(self):
        """
        Gets the model number of the remote control.

        :return: Remote model number.
        :rtype: str
        """
        return self.__sony_api.send(
            'system',
            'getRemoteControllerInfo'
        )[0]['type']


class SystemInformation(object):

    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, key):
        res = self.__sony_api.send('system', 'getSystemInformation')[0]

        if key in res:
            return res[key]
        else:
            raise UnsupportedError

    @property
    def product(self):
        """
        Gets the device category.

        :return: "TV" - Television device
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('product')

    @property
    def help_url(self):
        """
        Gets the help url for the device

        :return: url.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('helpUrl')

    @property
    def device_id(self):
        """
        Gets the general device ID for the device

        :return: device ID.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('deviceID')

    @property
    def version(self):
        """
        Gets the version information for the device

        :return: version information.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('version')

    @property
    def duid(self):
        """
        Gets the support DUID (DHCP Unique Identifier) for the device

        :return: DHCP Unique Identifier.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('duid')

    @property
    def wireless_mac_address(self):
        """
        Gets the wireless MAC address for the device

        :return: MAC address.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('wirelessMacAddr')

    @property
    def esn(self):
        """
        Gets the esn of the device for Netflix.

        :return: Model name (10 joists) and ID (22 joists).
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('esn')

    @property
    def icon_url(self):
        """
        Gets the icon URL of the service for the device.

        :return: icon url.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('iconUrl')

    @property
    def ssid(self):
        """
        Gets the network SSID of the access point to which the device is
        connected.

        :return: ssid.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('ssid')

    @property
    def blueteeth_address(self):
        """
        Gets the Bluetooth address of the device.

        :return: address.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('bdAddr')

    @property
    def initial_power_on_time(self):
        """
        Gets the initial power-on time for the device.

        :return: ISO8601 formatted date/time.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('initialPowerOnTime')

    @property
    def last_power_on_time(self):
        """
        Gets the last time the device was powered on.

        :return: ISO8601 formatted date/time.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('lastPowerOnTime')

    @property
    def blueteeth_id(self):
        """
        Gets the Bluetooth Low Energy ID for the device.

        :return: id.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('bleID')

    @property
    def mac(self):
        """
        Gets the ethernet mac id.

        :return: MAC address.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('macAddr')

    @property
    def name(self):
        """
        Gets the product name.

        :return: Product name.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('name')

    @property
    def language(self):
        """
        Gets the language code of the device.

        :return: Represented by ISO-639 alpha-3
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('language')

    @language.setter
    def language(self, value):
        """
        Sets the language code of the device.

        :param value: ISO-639 alpha-3 language code.
        :type value: str

        :return: None
        :rtype: None
        """
        self.__sony_api.send('system', 'setLanguage', language=value)

    @property
    def cid(self):
        """
        Gets the id to identify server device.

        Used for log upload system to identify that uploaded data is related
        to this device.

        :return: cid
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('cid')

    @property
    def generation(self):
        """
        Gets the rough age and season of the device.

        :return: Parameter is composed of "[X].[Y].[Z]", where [X], [Y] and [Z]
            are string representing integer and concatenated with period "." in
            between.
            The actual value is defined by each product and outside the scope
            of this document.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('generation')

    @property
    def region(self):
        """
        Gets the sales region of the device.

        :return: Represented by ISO-3166-1 alpha-3.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('region')

    @property
    def area(self):
        """
        Gets the country code of the device

        :return: Represented by ISO-3166-1 alpha-3
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('area')

    @property
    def model(self):
        """
        Gets the model name of the device.

        This must be unique within each product. The actual value is defined
        by each product and outside the scope of this document.

        :return: Model name.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('model')

    @property
    def serial(self):
        """
        Gets the serial id assigned to the device.

         The actual value is defined by each product and outside the scope of
         this document.

        :return: Serial number.
        :rtype: str
        :raises: UnsupportedError
        """
        return self.__send('serial')
