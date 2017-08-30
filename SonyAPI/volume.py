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

from api_const import PY2


class VolumeBase(object):
    def __init__(
        self,
        sony_api,
        target='speakers',
        minVolume=0,
        maxVolume=0,
        **kwargs
    ):
        self._sony_api = sony_api
        self.target = target
        self.min_volume = int(minVolume)
        self.max_volume = int(maxVolume)

    def _set_volume(self, value):
        volume = int(value)
        if volume < self.min_volume:
            volume = self.min_volume

        if volume > self.max_volume:
            volume = self.max_volume

        self._sony_api.send(
            'audio',
            'setAudioVolume',
            target=self.target,
            volume=str(volume)
        )

    @property
    def _volume(self):
        return int(self._volume_info['volume'])

    @property
    def _volume_info(self):
        results = self._sony_api.send('audio', 'getVolumeInformation')

        for result in results:
            if result['target'] == self.target:
                return result

    def up(self):
        self._set_volume(self._volume + 1)

    def down(self):
        self._set_volume(self._volume - 1)

    @property
    def mute(self):
        return self._volume_info['mute']

    @mute.setter
    def mute(self, status):
        if self._sony_api.power:
            self._sony_api.send('audio', 'setAudioMute', status=status)

    def toggle_mute(self):
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
        return self

    def __isub__(self, other):
        self._set_volume(self._volume - int(other))
        return self

    def __imul__(self, other):
        self._set_volume(self._volume * int(other))
        return self

    def __idiv__(self, other):
        self._set_volume(self._volume / int(other))
        return self

    def __float__(self):
        return float(self._volume)

    def __int__(self):
        return self._volume

    def __str__(self):
        return str(self._volume)

    if PY2:
        def __unicode__(self):
            return unicode(str(self))


class Volume(VolumeBase):
    def __init__(self, sony_api):
        self._sony_api = sony_api
        self._headphone = None
        self._speaker = None
        VolumeBase.__init__(self, sony_api)

        results = self._sony_api.send('audio', 'getVolumeInformation')
        for result in results:
            v_device = VolumeBase(sony_api, **result)
            setattr(self, '_' + result['target'], v_device)

    @property
    def speaker(self):
        return self._speaker

    @speaker.setter
    def speaker(self, value):
        self._speaker._set_volume(value)

    @property
    def headphone(self):
        return self._headphone

    @headphone.setter
    def headphone(self, value):
        self._headphone._set_volume(value)
