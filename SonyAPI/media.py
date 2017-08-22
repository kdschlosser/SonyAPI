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
from datetime import datetime

DATE = '%Y-%m-%dT%H:%M:%S'


class Media(object):

    def __init__(self, handler):
        self._handler = handler

    def __getitem__(self, item):
        return self._playing_info(item)

    def _playing_info(self, key):
        response = self._handler.send(
            "sony/avContent",
            "getPlayingContentInfo"
        )
        playing_content_data = response['result'][0]

        return playing_content_data[key]

    @property
    def now_playing(self):
        return dict(
            title=self.title,
            program_title=self.program_title,
            source=self.source
        )

    @property
    def program_title(self):
        return self._playing_info('programTitle')

    @property
    def title(self):
        return self._playing_info('title')

    @title.setter
    def title(self, title):
        for source in self._handler.source_list:
            if source['title'] == title:
                self._handler.send(
                    "sony/avContent",
                    "setPlayContent",
                    uri=source['uri']
                )

    @property
    def type(self):
        return self._playing_info('programMediaType')

    @property
    def display_number(self):
        return self._playing_info('dispNum')

    @property
    def source(self):
        return self._playing_info('source')

    @source.setter
    def source(self, source):
        self._handler.power = True
        source_list = self._handler.source_list
        if source in source_list:
            self.uri = source_list[source]

    @property
    def uri(self):
        return self._playing_info('uri')

    @uri.setter
    def uri(self, uri):
        self._handler.send(
            "sony/avContent",
            "setPlayContent",
            uri=uri
        )

    @property
    def duration(self):
        duration = time.gmtime(self._playing_info('durationSec'))

        def __str__():
            return time.strftime('%H:%M:%S', duration)

        duration.__str__ = __str__
        return duration

    @property
    def start_time(self):
        start_time = self._playing_info('startDateTime')
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
        start_time = self._playing_info('startDateTime')
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

