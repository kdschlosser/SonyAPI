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

import traceback
import json


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


class LOGGER(object):
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