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


class Volume(object):

    def __init__(self, parent, target):
        self._parent = parent
        self.name = target
        self._target = target

    @property
    def _volume_info(self):
        return self._parent.get_volume_data(self._target)

    @property
    def min_volume(self):
        return ['minVolume']

    @property
    def max_volume(self):
        return self._volume_info['maxVolume']

    @property
    def volume_up(self):
        if self._parent.power:
            self.volume = self.volume + 1
        return self.volume

    @property
    def volume_down(self):
        if self._parent.power:
            self.volume = self.volume - 1
        return self.volume

    @property
    def volume(self):
        if self._parent.power:
            return self._volume_info['volume']

    @volume.setter
    def volume(self, volume):
        if volume < self.min_volume:
            volume = self.min_volume

        if volume > self.max_volume:
            volume = self.max_volume

        if self._parent.power:
            json_data = self._parent.build_json(
                "setAudioVolume",
                dict(target=target, volume=volume)
            )
            self._parent.send("sony/audio", json_data)

    @property
    def mute(self):
        if self._parent.power:
            return self._volume_info['mute']

    @mute.setter
    def mute(self, state):
        if self._parent.power and state != self.mute:
            self._parent.ircc(self._parent.command('Mute'))
