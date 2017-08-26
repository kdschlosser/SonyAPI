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


class VolumeBase(object):
    target = 'speaker'

    def __init__(self, sony_api):
        self._sony_api = sony_api

    def _set_volume(self, value):
        if self._sony_api.power:
            volume = int(value)
            if volume < self.min_volume:
                volume = self.min_volume

            if volume > self.max_volume:
                volume = self.max_volume

            if self._sony_api.power:
                self._sony_api.send(
                    'audio',
                    'setAudioVolume',
                    target=self.target,
                    volume=volume
                )

    @property
    def _volume(self):
        if self._sony_api.power:
            return int(self._volume_info['volume'])
        else:
            return 0

    @property
    def _volume_info(self):
        results = self._sony_api.send('audio', 'getVolumeInformation')

        for result in results:
            if result['target'] == self.target:
                return result

    @property
    def min_volume(self):
        return self._volume_info['minVolume']

    @property
    def max_volume(self):
        return self._volume_info['maxVolume']

    def up(self):
        self._set_volume(self._volume + 1)
        return self._volume

    def down(self):
        self._set_volume(self._volume - 1)
        return self._volume

    @property
    def mute(self):
        if self._sony_api.power:
            return self._volume_info['mute']

    @mute.setter
    def mute(self, status):
        if self._sony_api.power:
            self._sony_api.send('audio', 'setAudioMute', status=status)

    def toggle_mute(self):
        if self._sony_api.power:
            self.mute = not self.mute

    def __lt__(self, other):
        return self._volume < int(other)

    def __le__(self, other):
        return self._volume <= int(other)

    def __eq__(self, other):
        return self._volume == int(other)

    def __ne__(self, other):
        return self._volume != int(other)

    def __gt__(self, other):
        return self._volume > int(other)

    def __ge__(self, other):
        return self._volume >= int(other)

    def __add__(self, other):
        return self._volume + int(other)

    def __sub__(self, other):
        return self._volume - int(other)

    def __mul__(self, other):
        return self._volume * int(other)

    def __div__(self, other):
        return self._volume / int(other)

    def __iadd__(self, other):
        self._set_volume(self._volume + int(other))

    def __isub__(self, other):
        self._set_volume(self._volume - int(other))

    def __imul__(self, other):
        self._set_volume(self._volume * int(other))

    def __idiv__(self, other):
        self._set_volume(self._volume / int(other))

    def __float__(self):
        return float(self._volume)

    def __int__(self):
        return self._volume

    def __str__(self):
        return str(self._volume)

    def __unicode__(self):
        return unicode(str(self))


class Speaker(VolumeBase):
    target = 'speaker'


class Headphone(VolumeBase):
    target = 'headphone'


class Volume(VolumeBase):
    def __init__(self, sony_api):
        self._sony_api = sony_api
        self._speaker = None
        self._headphone = None
        VolumeBase.__init__(self, sony_api)

    @property
    def speaker(self):
        if self._speaker is None:
            self._speaker = Speaker(self._sony_api)
        return self._speaker

    @speaker.setter
    def speaker(self, value):
        self.speaker._set_volume(value)

    @property
    def headphone(self):
        if self._headphone is None:
            self._headphone = Headphone(self._sony_api)
        return self._headphone

    @headphone.setter
    def headphone(self, value):
        self.headphone._set_volume(value)






