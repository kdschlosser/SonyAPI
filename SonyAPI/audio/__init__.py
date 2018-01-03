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
from . import sound, speaker, volume, equalizer


class Audio(object):

    def __init__(self, sony_api):
        self.__sony_api = sony_api
        self.__sound_settings = None
        self.__equalizer_settings = None
        self.__speaker_settings = None
        self.__volume = None

    def __send(self, method, **params):
        return self.__sony_api.send('audio', method, **params)

    @property
    def equalizer_settings(self):
        """
        Equalizer Settings.

        *Returns:*

            `SonyAPI.audio.equalizer.Settings` instance

        *Return type:*

            `SonyAPI.audio.equalizer.Settings`
        """
        if self.__equalizer_settings is None:
            self.__equalizer_settings = equalizer.Settings(self.__sony_api)
        return self.__equalizer_settings

    @property
    def volume(self):
        """
        Volume.

        *Returns:*

            `SonyAPI.audio.volume.Volume` instance

        *Return type:*

            `SonyAPI.audio.volume.Volume`
        """
        if self.__volume is None:
            self.__volume = volume.Volume(self.__sony_api)
        return self.__volume

    @property
    def sound_settings(self):
        """
        Sound Settings.

        *Returns:*

            `SonyAPI.audio.sound.Settings` instance

        *Return type:*

            `SonyAPI.audio.sound.Settings`
        """
        if self.__sound_settings is None:
            self.__sound_settings = sound.Settings(self.__sony_api)
        return self.__sound_settings

    @property
    def speaker_settings(self):
        """
        Speaker Settings.

        *Returns:*

            `SonyAPI.audio.speaker.Settings` instance

        *Return type:*

            `SonyAPI.audio.speaker.Settings`
        """
        if self.__speaker_settings is None:
            self.__speaker_settings = speaker.Settings(self.__sony_api)
        return self.__speaker_settings

