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

import time
import requests
from datetime import datetime
from cStringIO import StringIO

DATE = '%Y-%m-%dT%H:%M:%S'


def get_icon(url):
    icon_data = requests.get(url).content
    icon = StringIO()
    icon.write(icon_data)
    icon.seek(0)
    return icon


class PlayTimeMixin(object):
    _duration = 0
    _start_date_time = ''

    @property
    def duration(self):
        duration = time.gmtime(self._duration)

        def __str__():
            return time.strftime('%H:%M:%S', duration)

        duration.__str__ = __str__
        return duration

    @property
    def start_time(self):
        start_time = self._start_date_time
        try:
            start_time = (
                datetime.time(datetime.strptime(start_time[:-5], DATE))
            )
        except TypeError:
            start_time = datetime.time(
                datetime(*(time.strptime(start_time[:-5], DATE)[0:6]))
            )

        def __str__():
            return time.strftime('%H:%M:%S', start_time)

        start_time.__str__ = __str__
        return start_time

    @property
    def remaining(self):
        remaining = self.duration - self.elapsed

        def __str__():
            return time.strftime('%H:%M:%S', remaining)

        remaining.__str__ = __str__
        return remaining

    @property
    def elapsed(self):
        start_time = self._start_date_time
        try:
            elapsed = datetime.now() - datetime.strptime(start_time[:-5], DATE)
        except TypeError:
            elapsed = (
                datetime.now() -
                datetime(*(time.strptime(start_time[:-5], DATE)[0:6]))
            )

        def __str__():
            return time.strftime('%H:%M:%S', elapsed)

        elapsed.__str__ = __str__
        return elapsed

    @property
    def percent_elapsed(self):
        rounded_elapsed = (
            round(((self.elapsed.seconds / self.duration.seconds) * 100), 0)
        )
        percent_elapsed = int(rounded_elapsed)

        def __str__():
            return str(int(rounded_elapsed)) + '%'

        percent_elapsed.__str__ = __str__
        return percent_elapsed

    @property
    def end_time(self):
        end_time = self.start_time + self.duration

        def __str__():
            return time.strftime('%H:%M', end_time)

        end_time.__str__ = __str__
        return end_time
