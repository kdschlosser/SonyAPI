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


class CEC(object):

    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, method, **params):
        return self.__sony_api('cec', method, **params)[0]

    def mhl_power_feed_mode(self, value):
        """
        Sets MHL power feed mode.

        :param value: possible Values:
            True - enable power feed mode
            False - disable power feed mode
        :type value: bool

        :return: None
        :rtype: None
        """
        self.__send('setMhlPowerFeedMode', enabled=value)

    mhl_power_feed_mode = property(fset=mhl_power_feed_mode)

    def mhl_auto_input_change_mode(self, value):
        """
        Sets MHL auto input change mode

        :param value: possible Values:
            True - enable auto input change mode
            False - disable auto input change mode
        :type value: bool

        :return: None
        :rtype: None
        """
        self.__send('setMhlAutoInputChangeMode', enabled=value)

    mhl_auto_input_change_mode = property(fset=mhl_auto_input_change_mode)

    def control_mode(self, value):
        """
        Sets CEC control mode

        :param value: possible Values:
            True - accept control commands from CEC device.
            False - deny the commands.
        :type value: bool

        :return: None
        :rtype: None
        """
        self.__send('setCecControlMode', enabled=value)

    control_mode = property(fset=control_mode)

    def power_sync_mode(self, (on, off)):
        """
        Sets CEC control mode

        :param on: Power-On sync modes:
            True - when any CEC devices connected to this device are turned on,
            this device also automatically get turned on.
            False - this mode is disabled.
        :type on: bool
        :param off: Power-Off sync mode:
            True - when this device is turned off, CEC devices connected to
            this device also automatically get turned off.
            False - this mode is disabled.
        :type off: bool

        :return: None
        :rtype: None
        """

        self.__send(
            'setPowerSyncMode',
            sourcePowerOnSync=on,
            sinkPowerOffSync=off
        )

    power_sync_mode = property(fset=power_sync_mode)
