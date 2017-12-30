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

from __future__ import absolute_import
from . import sound, speaker, volume


class Audio(object):

    def __init__(self, sony_api):
        self.__sony_api = sony_api
        self._sound_settings = sound.Settings(sony_api)
        self._speaker_settings = speaker.Settings(sony_api)
        self._volume = volume.Volume(sony_api)

    def __send(self, method, **params):
        return self.__sony_api.send('audio', method, **params)

    @property
    def volume(self):
        return self._volume

    @property
    def sound_settings(self):
        return self._sound_settings

    @property
    def speaker_settings(self):
        return self._speaker_settings
