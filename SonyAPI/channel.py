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


class Channel(object):
    _sony_api = None

    def __get__(self, instance, owner):
        self._sony_api = instance
        return self

    def __set__(self, instance, value):
        self._sony_api = instance

        for channel in self._channel_lineup:
            if value in channel:
                self._set_channel(channel[0])

    def _set_channel(self, value):
        if self._sony_api.power:
            self._sony_api.play_tv_content(channel=str(value))

    @property
    def _channel(self):
        if self._sony_api.power:
            return self._sony_api.playing_content.display_num
        else:
            return None

    @property
    def _channel_lineup(self):
        results = []
        for channel in self.lineup:
            results += [[channel.display_num, channel.channel_name]]
        return results

    @property
    def lineup(self):
        for item in self._sony_api.content_list:
            if item.source.startswith('tv'):
                yield item

    def up(self):
        channel = self._channel
        new_channel = '999999999'

        for display_num, _ in self._channel_lineup:
            if new_channel > display_num > channel:
                new_channel = display_num

        if new_channel == '999999999':
            for display_num, _ in self._channel_lineup:
                if new_channel > display_num:
                    new_channel = display_num

        self._set_channel(new_channel)
        return self._channel

    def down(self):
        channel = self._channel
        new_channel = '000000000'

        for display_num, _ in self._channel_lineup:
            if new_channel < display_num < channel:
                new_channel = display_num

        if new_channel == '000000000':
            for display_num, _ in self._channel_lineup:
                if new_channel < display_num:
                    new_channel = display_num

        self._set_channel(new_channel)
        return self._channel

    def __lt__(self, other):
        return self._channel < str(other)

    def __le__(self, other):
        return self._channel <= str(other)

    def __eq__(self, other):
        return self._channel == str(other)

    def __ne__(self, other):
        return self._channel != str(other)

    def __gt__(self, other):
        return self._channel > str(other)

    def __ge__(self, other):
        return self._channel >= str(other)

    def __add__(self, other):
        return self._channel + str(other)

    def __sub__(self, other):
        return self._channel - str(other)

    def __mul__(self, other):
        return self._channel * str(other)

    def __div__(self, other):
        return self._channel / str(other)

    def __iadd__(self, other):
        self._set_channel(int(self._channel) + int(other))

    def __isub__(self, other):
        self._set_channel(int(self._channel) - int(other))

    def __imul__(self, other):
        self._set_channel(int(self._channel) * int(other))

    def __idiv__(self, other):
        self._set_channel(int(self._channel) / int(other))

    def __int__(self):
        return self._channel

    def __str__(self):
        return self._channel

    def __unicode__(self):
        return unicode(str(self))
