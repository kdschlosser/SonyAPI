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


class Channels(object):

    def __init__(self, sony_api):
        self._sony_api = sony_api

    @property
    def _channel(self):
        return self._sony_api.now_playing.display_num

    @property
    def lineup(self):
        results = []
        for item in self._sony_api.content_list:
            if item.uri.startswith('tv'):
                results += [item]

        return results

    def _set_channel(self, direction, channel):
        for chan in self.lineup:
            if chan.display_num == str(channel):
                chan.set()
                return channel

        selected_channel = None
        new_channel = 999999 if direction == 'up' else 0

        for chan in self.lineup:
            if direction == 'up':
                if (
                    new_channel >
                    int(chan.display_num) >
                    channel
                ):
                    selected_channel = chan
                    new_channel = int(chan.display_num)
            else:
                if (
                    new_channel <
                    int(chan.display_num) <
                    channel
                ):
                    selected_channel = chan
                    new_channel = int(chan.display_num)

        if new_channel == 999999999:
            for chan in self.lineup:
                if new_channel > int(chan.display_num):
                    selected_channel = chan
                    new_channel = int(chan.display_num)

        if new_channel == 0:
            for chan in self.lineup:
                if new_channel < int(chan.display_num):
                    selected_channel = chan
                    new_channel = int(chan.display_num)

        if selected_channel is not None:
            selected_channel.set()
        return selected_channel

    def up(self):
        return self._set_channel('up', int(self._channel) + 1)

    def down(self):
        return self._set_channel('down', int(self._channel) - 1)

    def __lt__(self, other):
        return int(self._channel) < int(other)

    def __le__(self, other):
        return int(self._channel) <= int(other)

    def __eq__(self, other):
        return int(self._channel) == int(other)

    def __ne__(self, other):
        return int(self._channel) != int(other)

    def __gt__(self, other):
        return int(self._channel) > int(other)

    def __ge__(self, other):
        return int(self._channel) >= int(other)

    def __add__(self, other):
        return int(self._channel) + int(other)

    def __sub__(self, other):
        return int(self._channel) - int(other)

    def __mul__(self, other):
        return int(self._channel) * int(other)

    def __div__(self, other):
        return int(self._channel) / int(other)

    def __iadd__(self, other):
        return self._set_channel('up', int(self._channel) + int(other))

    def __isub__(self, other):
        return self._set_channel('down', int(self._channel) - int(other))

    def __imul__(self, other):
        return self._set_channel('up', int(self._channel) * int(other))

    def __idiv__(self, other):
        return self._set_channel('down', int(self._channel) / int(other))

    def __int__(self):
        return int(self._channel)

    def __str__(self):
        return str(self._channel)

    def __unicode__(self):
        return unicode(str(self))
