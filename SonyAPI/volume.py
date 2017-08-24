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


class VolumeDevice(object):

    def __init__(self, sony_api, target):
        self._sony_api = sony_api
        self.target = target

    @property
    def _volume_info(self):
        results = self._sony_api.send('sony/audio', 'getVolumeInformation')

        for result in results:
            if result['target'] == self.target:
                return result

    @property
    def min_volume(self):
        return self._volume_info['minVolume']

    @property
    def max_volume(self):
        return self._volume_info['maxVolume']

    @property
    def volume_up(self):
        if self._sony_api.power:
            self.volume = self.volume + 1
        return self.volume

    @property
    def volume_down(self):
        if self._sony_api.power:
            self.volume = self.volume - 1
        return self.volume

    @property
    def volume(self):
        if self._sony_api.power:
            return self._volume_info['volume']

    @volume.setter
    def volume(self, volume):
        if volume < self.min_volume:
            volume = self.min_volume

        if volume > self.max_volume:
            volume = self.max_volume

        if self._sony_api.power:
            self._sony_api.send(
                'sony/audio',
                'setAudioVolume',
                target=self.target,
                volume=volume
            )

    @property
    def mute(self):
        if self._sony_api.power:
            return self._volume_info['mute']

    @mute.setter
    def mute(self, status):
        if self._sony_api.power:
            self._sony_api.send('sony/audio', 'setAudioMute', status=status)
