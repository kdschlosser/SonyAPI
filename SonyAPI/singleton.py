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


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = {}

        if (args, kwargs) not in cls._instances[cls]:
            cls._instances[cls][(args, kwargs)] = super(
                Singleton,
                cls
            ).__call__(*args, **kwargs)

        return cls._instances[cls][(args, kwargs)]


class ScheduleSingleton(type):
    _instances = {}

    def __call__(
        cls,
        id,
        title,
        startDateTime,
        durationSec,
        repeatType,
        type,
        uri,
        *args,
        **kwargs
    ):

        key = (id, title, startDateTime, durationSec, repeatType, type, uri)
        if cls not in cls._instances:
            cls._instances[cls] = {}

        if key not in cls._instances[cls]:
            cls._instances[cls][key] = super(ScheduleSingleton, cls).__call__(
                id,
                title,
                startDateTime,
                durationSec,
                repeatType,
                type,
                uri,
                *args,
                **kwargs
            )

        return cls._instances[cls][key]


class BrowserSingleton(type):
    _instances = {}

    def __call__(cls, url, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = {}

        if url not in cls._instances[cls]:
            cls._instances[cls][url] = super(
                BrowserSingleton,
                cls
            ).__call__(url, *args, **kwargs)

        return cls._instances[cls][url]
