# -*- coding: utf-8 -*-
#
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


from logger import LOGGER as _LOGGER
import json


class SonyAPIError(Exception):
    __module__ = 'SonyAPI'

    def __init__(self, msg):
        if isinstance(msg, dict):
            msg = json.dumps(msg, indent=4)

        _LOGGER.error(self.__class__.__name__, msg)
        self.msg = msg

    def __str__(self):
        return self.msg


class PinError(SonyAPIError):
    __module__ = 'SonyAPI'


class RegisterTimeoutError(SonyAPIError):
    __module__ = 'SonyAPI'


class NotImplementedError(SonyAPIError):
    # 501,"Not Implemented"
    __module__ = 'SonyAPI'


class UnsupportedError(SonyAPIError):
    # 15, "unsupported"
    __module__ = 'SonyAPI'


class JSONRequestError(SonyAPIError):
    __module__ = 'SonyAPI'
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
    __module__ = 'SonyAPI'


class VolumeDeviceError(SonyAPIError):
    __module__ = 'SonyAPI'


class RegisterError(SonyAPIError):
    __module__ = 'SonyAPI'


class IRCCError(SonyAPIError):
    __module__ = 'SonyAPI'


class SendError(SonyAPIError):
    __module__ = 'SonyAPI'


class IPAddressError(SonyAPIError):
    __module__ = 'SonyAPI'
