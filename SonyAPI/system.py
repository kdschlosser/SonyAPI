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

        :return: `SonyAPI.system.NetworkSettings` instance
        :rtype: `SonyAPI.system.NetworkSettings`
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

        :return: `SonyAPI.system.InterfaceInformation` instance
        :rtype: `SonyAPI.system.InterfaceInformation`
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

        :return: `SonyAPI.system.SystemInformation` instance
        :rtype: `SonyAPI.system.SystemInformation`
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

        :return: `SonyAPI.system.SystemSupportedFunction` instance
        :rtype: `SonyAPI.system.SystemSupportedFunction`
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

        :return: `SonyAPI.container.Container` instance that holds information about an available update.
        :rtype: `SonyAPI.container.Container`
        """
        result = self.__send('getSWUpdateInfo', network=True)[0]['swInfo']
        return container.Container(**result)

    @property
    def sleep_timer(self):
        """
        Sleep timer.

        **Getter:** Gets the sleep timer.

            *Returns:*

                * ``120`` - After 120 minutes.
                * ``90`` - After 90 minutes.
                * ``80`` - After 80 minutes.
                * ``70`` - After 70 minutes.
                * ``60`` - After 60 minutes.
                * ``50`` - After 50 minutes.
                * ``40`` - After 40 minutes.
                * ``30`` - After 30 minutes.
                * ``20`` - After 20 minutes.
                * ``10`` - After 10 minutes.
                * ``0`` - Do not automatically turn off.

            *Return type:* `int`

        **Setter:** Sets the sleep timer.

            *Accepted values:*

                * ``120`` - After 120 minutes.
                * ``90`` - After 90 minutes.
                * ``80`` - After 80 minutes.
                * ``70`` - After 70 minutes.
                * ``60`` - After 60 minutes.
                * ``50`` - After 50 minutes.
                * ``40`` - After 40 minutes.
                * ``30`` - After 30 minutes.
                * ``20`` - After 20 minutes.
                * ``10`` - After 10 minutes.
                * ``0`` - Do not automatically turn off.

            *Value type:* `int`
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
        Postal code.

        **Getter:** Gets the device postal code.

            *Returns:* Postal code.

            *Return type:* `str`

        **Setter:** Sets the device postal code.

            *Accepted value:* Postal code.

            *Value type:* `str`
        """
        return self.__send('getPostalCode')[0]['postalCode']

    @postal_code.setter
    def postal_code(self, value):
        self.__send('setPostalCode', postalCode=value)

    @property
    def time(self):
        """
        Sleep timer.

        **Getter:** Gets the current device time.

            *Returns:* `datetime.datetime` instance

            *Return type:* `datetime.datetime`

        **Setter:** Sets the device time.

            *Accepted value:* `datetime.datetime` instance

            *Value type:* `datetime.datetime`
        """
        res = self.__send('getCurrentTime')[0]

        if isinstance(res, dict):
            date_time = res['datetime']
        else:
            date_time = res

        return datetime.strptime(date_time, '%Y-%M-%DT%H:%M:%S%z')

    @time.setter
    def time(self, value=datetime.now()):
        self.__send(
            'setCurrentTime',
            dateTime=value.strftime('%Y-%M-%DT%H:%M:%S%z')
        )

    @property
    def color_keys_layout(self):
        """
        Gets color keys layout.

        :return: Color key layout information of remote controller.

            Examples:

                ``"BRGY"``

                ``"RGYB"``

            * ``"B"`` - Blue key.
            * ``"R"`` - Red key.
            * ``"G"`` - Green key.
            * ``"Y"`` - Yellow key.

        :rtype: str

        """
        return self.__send('getColorKeysLayout')[0]['colorKeysLayout']

    @property
    def power_saving_mode(self):
        """
        Power saving mode.

        **Getter:** Gets the power saving mode.

            *Returns:*

                * ``"off"`` - Power saving mode is disabled.
                * ``"low"`` - Power saving mode is enabled with level low.
                * ``"high"`` - Power saving mode is enabled with level high.
                * ``"pictureOff"`` - Power saving mode is enabled with panel output off.

            *Return type:* `str`

        **Setter:** Sets the power saving mode.

            *Accepted values:*

                * ``"off"`` - Power saving mode is disabled.
                * ``"low"`` - Power saving mode is enabled with level low.
                * ``"high"`` - Power saving mode is enabled with level high.
                * ``"pictureOff"`` - Power saving mode is enabled with panel output off.

            *Value type:* `str`
        """
        return self.__send('getPowerSavingMode')[0]['mode']

    @power_saving_mode.setter
    def power_saving_mode(self, value):
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

        :param value:
            *Accepted values:*

                * ``True`` - LED is enabled.
                * ``False`` - LED is disabled.

        :type value: bool

        :return: None
        :rtype: None
        """
        self.__send(
            'setLEDIndicatorStatus',
            status='on' if value else 'off',
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
        Front panel brightness.

        **Getter:** Gets the front panel brightness.

            *Returns:*

                * ``"bright"`` - Front panel brightness is bright.
                * ``"dark"`` - Front panel brightness is dark.
                * ``"off"`` - Front panel brightness is off.

            *Return type:* `str`
        """
        return self.__send('FrontPanelBrightness')

    @property
    def av_separation(self):
        """
        AV separation.

        **Getter:** Gets the AV separation.

            *Returns:*

                * ``True`` - Output data in the AV Separation Output Mode.
                * ``False`` - Output data in the Multi Output Mode.

            *Return type:* `bool`
        """
        return self.__send('AVSeparation') == 'on'

    @property
    def auto_display(self):
        """
        Auto display.

        **Getter:** Gets the Auto display.

            *Returns:*

                * ``True`` - OSD is displayed automatically when state or mode etc... is changed.
                * ``False`` - OSD is displayed only by user operation.

            *Return type:* `bool`
        """
        return self.__send('AutoDisplay') == 'on'

    @property
    def screen_saver(self):
        """
        Screen saver mode.

        **Getter:** Gets the Screen saver mode.

            *Returns:*

                * ``True`` - Enable Screen Saver.
                * ``False`` - Disable Screen Saver.

            *Return type:* `bool`
        """
        return self.__send('ScreenSaver') == 'on'

    @property
    def software_update_notification(self):
        """
        Software update notification mode.

        **Getter:** Gets the Software update notification mode.

            *Returns:*

                * ``True`` - Enable Network update notification function.
                * ``False`` - Disable Network update notification function.

            *Return type:* `bool`
        """
        return self.__send('SoftwareUpdateNotification') == 'on'

    @property
    def rich_meta_information(self):
        """
        Rich meta information (Gracenote) settings.

        **Getter:** Gets the rich meta information (Gracenote) settings.

            *Returns:*

                * ``"auto"`` - Obtains information from Gracenote.

                    When playback is stopped, BD ROM/DVD ROM creates TOC for
                    Gracenote connection and obtains information from
                    Gracenote. Whereas CD DA creates TOC and obtains
                    information from Gracenote upon mounting.

                * ``"manual"`` - Gracenote only.

                    Creates TOC and obtains information from Gracenote only
                    when there is a request for information acquisition, such
                    as window display.

            *Return type:* `str`
        """
        return self.__send('RichMetaInformation')

    @property
    def auto_renderer(self):
        """
        Auto renderer.

        **Getter:** Gets the auto renderer.

            Access permission setting value required when registering new
            DMC/+PU+, DMR and DMP.

            *Returns:*

                * ``True`` - Access Permission as "Allow" state.

                    When there is an access from new DMC/+PU+ (Send contents
                    etc.), DMR and DMP registers Access Permission as "Allow"
                    state. When it exceeds the max number of possible Access
                    Permissions, is registers Access Permission as
                    "Block(Hold)" state.

                * ``False`` - Access Permission as "Block(Hold)" state.

                    When there is an access from new DMC/+PU+ (Send contents
                    etc.), DMR and DMP registers Access Permission as
                    "Block(Hold)" state.

            *Return type:* `bool`
        """
        return self.__send('AutoRenderer') == 'on'

    @property
    def name_of_device(self):
        """
        Device name.

        **Getter:** Gets the name of the device.

            *Returns:*

                Example: ``"BD Player in Living"``

            *Return type:* `str`
        """
        return self.__send('NameDevice')

    @property
    def ir_repeat(self):
        """
        IR Repeat.

        **Getter:** Gets the IR Repeat.

            Whether a server receives and sends IR signal to other device.

            *Returns:*

                * ``True`` - A server receives and sends IR signal for other device.
                * ``False`` - A server does not receive and send IR signal to other device.

            *Return type:* `bool`
        """
        return self.__send('IRRepeat') == 'on'

    @property
    def cis_ip_control(self):
        """
        CIS-IP Control.

        **Getter:** Gets the CIS-IP Control.

            Whether a dedicated controller (home automation controller) on the
            home network is allowed to control a device by CIS-IP control.

            *Returns:*

                * ``True`` - Enable CIS-IP control function.
                * ``False`` - Disable CIS-IP control function.

            *Return type:* `bool`
        """
        return self.__send('CIS-IPControl') == 'on'

    @property
    def auto_update(self):
        """
        Auto Update.

        **Getter:** Gets the Auto Update.

            Whether to enable auto software update function or not.

            *Returns:*

                * ``True`` - Enable Auto SW Update function.
                * ``False`` - Disable Auto SW Update function.

            *Return type:* `bool`
        """
        return self.__send('AutoUpdate') == 'on'

    @property
    def time_zone_settings(self):
        """
        Time Zone settings.

        **Getter:** Gets the Time Zone settings.

            Set Time Zone unique name (Area/Location) used in tz database
            or offset value is also able to be added by the following format.
            <Time Zone unique name used in tz database>|<optional offset value (minutes)>

            *Returns:*

                Examples:

                    ``"America/New_York|-240"``

                    ``"Asia/Tokyo|540"``

            *Return type:* `str`
        """
        return self.__send('TimeZone')

    @property
    def osd_language(self):
        """
        OSD Language.

        **Getter:** Gets the OSD Language.

            OSD language code represented by BCP47 (RFC4646 and RFC4647)

            *Returns:*

                Examples:

                    ``"ja"``

                    ``"en-US"``

            *Return type:* `str`
        """
        return self.__send('OSDLanguage')

    @property
    def client_language(self):
        """
        Client Language.

        **Getter:** Gets the Client Language.

            Client language code represented by BCP47 (RFC4646 and RFC4647)

            *Returns:*

                Examples:

                    ``"ja"``

                    ``"en-US"``

            *Return type:* `str`
        """
        return self.__send('ClientLanguage')

    @property
    def quick_start_mode(self):
        """
        Quick Start Mode.

        **Getter:** Gets the Quick Start Mode.

            Whether to set Standby mode during Power Off or not.

            *Returns:*

                * ``True`` - Standby mode is set during Power Off.
                * ``False`` - Standby mode is not set during Power Off.

            *Return type:* `bool`
        """
        return self.__send('QuickStart') == 'on'

    @property
    def auto_standby(self):
        """
        Auto Standby.

        This device automatically changes to Power OFF, when judged that there
        is no operation for a certain period of time.

        **Getter:** Gets the Auto Standby Mode.

            Whether to Auto Standby feature or not.

            *Returns:*

                * ``True`` - Enable Auto Standby.
                * ``False`` - Disable Auto Standby.

            *Return type:* `bool`
        """
        return self.__send('AutoStandby') == 'on'

    @property
    def network_standby_mode(self):
        """
        Network Standby.

        When a device is Network standby state, network is available even in
        power off state.

        **Getter:** Gets the Network Standby Mode.

            Whether to enable Network standby mode.

            *Returns:*

                * ``True`` - Enable Network Standby.
                * ``False`` - Disable Network Standby.

            *Return type:* `bool`
        """
        return self.__send('NetworkStandby') == 'on'

    @property
    def secure_link_mode(self):
        """
        Secure Link.

        Secure Link to a specific surround amplifier in range of wireless
        reception.

        **Getter:** Gets the Secure Link Mode.

            *Returns:*

                * ``True`` - Enable Secure Link function.
                * ``False`` - Disable Secure Link function.

            *Return type:* `bool`
        """
        return self.__send('SecureLink') == 'on'

    @property
    def rf_band(self):
        """
        RF Band.

        **Getter:** Gets the RF Band.

            RF Band which RF Channel belongs to.

            *Returns:*

                * ``"auto"`` - Set the value of RF Band automatically.
                * ``"5.2GHz"`` - Set 5.2GHz as RF Band.
                * ``"5.8GHz"`` - Set 5.8GHz as RF Band.

            *Return type:* `str`
        """
        return self.__send('RFBand')

    @property
    def rf_channel(self):
        """

        RF Channel.

        **Getter:** Gets the RF Channel.

            *Returns:*

                * ``"auto"`` - Set the value of RF Channel automatically.
                * ``1`` - Set 1 channel as RF Channel.
                * ``2`` - Set 2 channel as RF Channel.
                * ``3`` - Set 3 channel as RF Channel.

            *Return type:* `str`, `int`
        """
        return self.__send('RFChannel')

    @property
    def sleep_timer(self):
        """
        Sleep timer.

        Sleep Timer (min) to turn off automatically at a specified time.

        **Getter:** Gets the sleep timer.

            *Returns:*

                * ``120`` - After 120 minutes.
                * ``90`` - After 90 minutes.
                * ``80`` - After 80 minutes.
                * ``70`` - After 70 minutes.
                * ``60`` - After 60 minutes.
                * ``50`` - After 50 minutes.
                * ``40`` - After 40 minutes.
                * ``30`` - After 30 minutes.
                * ``20`` - After 20 minutes.
                * ``10`` - After 10 minutes.
                * ``0`` - Do not automatically turn off.
                * ``None`` - Sleep timer settings unknown.

            *Value type:* `int`, `None`
        """
        res = self.__send('SleepTimer')


        if res is None:
            return None
        if res == 'off':
            return 0
        return int(res)

    @property
    def privacy_setting(self):
        """
        Privacy Setting.

        **Getter:** Gets the Privacy Setting.

            Whether to enable Privacy setting or not.

            *Returns:*

                * ``True`` - Enable Privacy setting.
                * ``False`` - Disable Privacy setting.

            *Return type:* `bool`
        """
        return self.__send('PrivacySetting') == 'on'

    @property
    def activate_status(self):
        """
        Activate status.

        Activate status of Cast for Audio.

        **Getter:** Gets the Activate status.

            *Returns:*

                * ``True`` - Enable Activate status.
                * ``False`` - Disable Activate status.

            *Return type:* `bool`
        """
        return self.__send('ActivateStatus') == 'on'

    @property
    def current_cast(self):
        """
        Cast for Audio service version.

        Current Cast for Audio service version information.

        **Getter:** Gets the Activate status.

            *Returns:*

                Example: ``"Ver.xxx"``

            *Return type:* `str`
        """
        return self.__send('CurrentCastforAudio')

    @property
    def remote_device_permission(self):
        """
        Remote device permission settings.

        **Getter:** Gets the Remote device permission setting.

            Whether to permit access from remote device, which can access
            server device from outside the door.

            *Returns:*

                * ``True`` - Access permitted.
                * ``False`` - Access not permitted.

            *Return type:* `bool`
        """
        return self.__send('RemoteDevicePermission') == 'on'

    @property
    def wol_mac(self):
        """
        MAC address for WOL.

        This is just in case the WOL is software set

        **Getter:** Gets the MAC address for WOL.

            *Returns:*

                Example: ``"00:00:00:00:00:00"``

            *Return type:* `str`
        """
        return self.__send('WOL')

    @property
    def chinese_software_keyboard_supported(self):
        """
        Chinese software keyboard.

        **Getter:** Gets the device supports chinese software keyboard.

            *Returns:*

                * ``True`` - Supports.
                * ``False`` - No support.

            *Return type:* `bool`
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
        IP version 4 address.

        **Getter:** Gets the IP version 4 address.

            *Returns:*

                Example: ``"192.168.0.0"``

            *Return type:* `str`
        """
        return self.__send('ipAddrV4')

    @property
    def netif(self):
        """
        Network interface name.

        **Getter:** Gets the network interface name.

            *Returns:*

                Example: ``"eth0"``

            *Return type:* `str`
        """
        return self.__send('netif')

    @property
    def ipv6(self):
        """
        IP version 6 address.

        **Getter:** Gets the IP version 6 address.

            *Returns:*

                Example: ``"2001:0db8:85a3:0000:0000:8a2e:0370:7334"``

            *Return type:* `str`
        """
        return self.__send('ipAddrV6')

    @property
    def subnet_mask(self):
        """
        Subnet mask.

        **Getter:** Gets the subnet mask.

            *Returns:*

                Example: ``"255.255.255.0"``

            *Return type:* `str`
        """
        return self.__send('netmask')

    @property
    def dns(self):
        """
        DNS servers.

        **Getter:** Gets the DNS servers.

            *Returns:*

                Example: ``["8.8.8.8"``, ``"8.8.4.4"]``

            *Return type:* `list`
        """
        return self.__send('dns')

    @property
    def mac(self):
        """
        Hardware address.

        **Getter:** Gets the hardware address.

            *Returns:*

                Example: ``"00:00:00:00:00:00"``

            *Return type:* `str`
        """
        return self.__send('hwAddr')

    @property
    def gateway(self):
        """
        Default gateway address.

        **Getter:** Gets the default gateway address.

            *Returns:*

                Example: ``"192.168.1.1"``

            *Return type:* `str`
        """
        return self.__send('gateway')

    @property
    def wol(self):
        """
        Wake On Lan (WOL) state.

        **Getter:** Gets the Wake On Lan (WOL) state.

            *Returns:*

                * ``True`` - WOL is enabled.
                * ``False`` - WOL is disabled.

            *Return type:* `bool`

        **Setter:** Sets the Wake On Lan (WOL) state.

            *Accepted values:*

                * ``True`` - WOL is enabled.
                * ``False`` - WOL is disabled.

            *Value type:* `bool`
        """
        return self.__sony_api.send('system', 'getWolMode')[0]['enabled']

    @wol.setter
    def wol(self, value):
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
        Server name.

        In case device can launch multiple Scalar WebAPI servers, return this
        server's name for client to distinguish.

        **Getter:** Gets the Server name.

            *Returns:* Server name.

            *Return type:* `str`
        """
        return self.__send('serverName')

    @property
    def model_name(self):
        """
        Model name.

        **Getter:** Gets the Model name.

            *Returns:* Model name.

            *Return type:* `str`
        """
        return self.__send('modelName')

    @property
    def product_name(self):
        """
        Product name.

        **Getter:** Gets more detailed product information.

            *Returns:* Product name.

            *Return type:* `str`
        """
        return self.__send('productName')

    @property
    def product_category(self):
        """
        Category name.

        **Getter:** Gets the Category name.
            *Returns:*

                * ``"camera"`` - Cameras and Camcorders.
                * ``"tv"`` - TV.
                * ``"internetTV"`` - Internet player with Google TV.
                * ``"videoServer"`` - The device that can serve downloadable video contents.
                * ``"homeTheaterSystem"`` - Home theater system.
                * ``"videoPlayer"`` - Video Player.
                * ``"personalAudio"`` - Personal Audio product.

            *Return type:* `str`
        """
        return self.__send('productCategory')

    @property
    def version(self):
        """
        Interface version.

        Version for client to change its behavior w.r.t significant difference
        within productCategory. This version is managed/controlled within each
        productCategory.

        **Getter:** Gets the Interface version.

            *Returns:* Value is composed of ``"[X].[Y].[Z]"``

                Where ``[X]``, ``[Y]`` and ``[Z]`` are string representing
                integer and concatenated with period "." in between.

                ``[X]`` - This value is assigned and incremented so that
                client can distinguish any significant difference of device or
                group of devices within productCategory. How this value is
                assigned depends on each productCategory.

                ``[Y]`` - This value represents the version of API sets. This
                version must be incremented in case supported APIs are added
                or deleted.

                ``[Z]`` - This value must be incremented in case any behavior
                of existing APIs are changed within [X.Y].

                Example: ``"1.4.6"``

            *Return type:* `str`
        """
        return self.__send('interfaceVersion')

    @property
    def remote_model(self):
        """
        Remote model number.

        **Getter:** Gets the Remote model number.

            *Returns:* Model number.

            *Return type:* `str`
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
        Device category.

        **Getter:** Gets the Device category.

            *Returns:* ``"TV"`` - Television device

            *Return type:* `str`
        """
        return self.__send('product')

    @property
    def help_url(self):
        """
        Help URL.

        **Getter:** Gets the Help URL.

            *Returns:* URL

            *Return type:* `str`
        """
        return self.__send('helpUrl')

    @property
    def device_id(self):
        """
        Device ID.

        **Getter:** Gets the Device ID.

            *Returns:* ID

            *Return type:* `str`
        """
        return self.__send('deviceID')

    @property
    def version(self):
        """
        Version information.

        **Getter:** Gets the Version information.

            *Returns:* Version.

            *Return type:* `str`
        """
        return self.__send('version')

    @property
    def duid(self):
        """
        Support DUID.

        DHCP Unique Identifier for the device

        **Getter:** Gets the Support DUID.

            *Returns:* DHCP Unique Identifier.

            *Return type:* `str`
        """
        return self.__send('duid')

    @property
    def wireless_mac_address(self):
        """
        Wireless MAC address.

        **Getter:** Gets the Wireless MAC address.

            *Returns:* ``"00:00:00:00:00:00"`` (example).

            *Return type:* `str`
        """
        return self.__send('wirelessMacAddr')

    @property
    def esn(self):
        """
        Netflix device ESN.

        **Getter:** Gets the Wireless MAC address.

            *Returns:* Model name (10 joists) and ID (22 joists).

            *Return type:* `str`
        """
        return self.__send('esn')

    @property
    def icon_url(self):
        """
        Icon URL.

        **Getter:** Gets the icon URL of the service for the device.

            *Returns:* URL.

            *Return type:* `str`
        """
        return self.__send('iconUrl')

    @property
    def ssid(self):
        """
        Network SSID.

        **Getter:** Gets the network SSID of the access point to which the device is connected.

            *Returns:* SSID.

            *Return type:* `str`
        """
        return self.__send('ssid')

    @property
    def blueteeth_address(self):
        """
        Blueteeth address.

        **Getter:** Gets the Blueteeth address of the device.

            *Returns:* BT address.

            *Return type:* `str`
        """
        return self.__send('bdAddr')

    @property
    def initial_power_on_time(self):
        """
        Initial power-on time.

        **Getter:** Gets the initial power-on time for the device.

            *Returns:* ISO8601 formatted date/time.

            *Return type:* `str`
        """
        return self.__send('initialPowerOnTime')

    @property
    def last_power_on_time(self):
        """
        Last power-on time.

        **Getter:** Gets the last time the device was powered on.

            *Returns:* ISO8601 formatted date/time.

            *Return type:* `str`
        """
        return self.__send('lastPowerOnTime')

    @property
    def blueteeth_id(self):
        """
        Blueteeth Low Energy ID.

        **Getter:** Gets the Blueteeth Low Energy ID for the device.

            *Returns:* ID.

            *Return type:* `str`
        """
        return self.__send('bleID')

    @property
    def mac(self):
        """
        Ethernet MAC address.

        **Getter:** Gets the Ethernet MAC address.

            *Returns:* ``"00:00:00:00:00:00"`` (example).

            *Return type:* `str`
        """
        return self.__send('macAddr')

    @property
    def name(self):
        """
        Product name.

        **Getter:** Gets the Product name.

            *Returns:* Name.

            *Return type:* `str`
        """
        return self.__send('name')

    @property
    def language(self):
        """
        Language.

        **Getter:** Gets the labguage code.

            *Returns:* Represented by ISO-639 alpha-3.

            *Return type:* `str`


        **Setter:** Sets the language code.

            *Accepted value:* ISO-639 alpha-3 language code.

            *Value type:* `str`
        """
        return self.__send('language')

    @language.setter
    def language(self, value):
        self.__sony_api.send('system', 'setLanguage', language=value)

    @property
    def cid(self):
        """
        ID to identify server device.

        Used for log upload system to identify that uploaded data is related
        to this device.

        **Getter:** Gets the id to identify server device.

            *Returns:* CID.

            *Return type:* `str`
        """
        return self.__send('cid')

    @property
    def generation(self):
        """
        Device build generation

        **Getter:** Gets the rough age and season of the device.

            *Returns:* Parameter is composed of ``"X.Y.Z"``

                Where [``X``], [``Y``] and [``Z``] are string representing
                integer and concatenated with period ``"."`` in between. The
                actual value is defined by each product and outside the scope
                of this document.

                Example: ``"1.5.4"``

            *Return type:* `str`
        """
        return self.__send('generation')

    @property
    def region(self):
        """
        Sales region

        **Getter:** Gets the sales region of the device.

            *Returns:* Represented by ISO-3166-1 alpha-3.

            *Return type:* `str`
        """
        return self.__send('region')

    @property
    def area(self):
        """
        Country code.

        **Getter:** Gets the country code of the device

            *Returns:* Represented by ISO-3166-1 alpha-3.

            *Return type:* `str`
        """
        return self.__send('area')

    @property
    def model(self):
        """
        Model name.

        **Getter:** Gets the model name of the device.

            *Returns:* This must be unique within each product.

                The actual value is defined by each product and outside the
                scope of this document.

            *Return type:* `str`
        """
        return self.__send('model')

    @property
    def serial(self):
        """
        Serial id.

        **Getter:** Gets the serial id assigned to the device.

            *Returns:* This must be unique within each product.

                The actual value is defined by each product and outside the
                scope of this document.

            *Return type:* `str`
        """
        return self.__send('serial')
