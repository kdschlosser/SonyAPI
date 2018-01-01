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

"""
notifyVolumeInformation
"""


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
        if self.__equalizer_settings is None:
            self.__equalizer_settings = EqualizerSettings(self.__sony_api)
        return self.__equalizer_settings

    @property
    def volume(self):
        if self.__volume is None:
            self.__volume = volume.Volume(self.__sony_api)
        return self.__volume

    @property
    def sound_settings(self):
        if self.__sound_settings is None:
            self.__sound_settings = sound.Settings(self.__sony_api)
        return self.__sound_settings

    @property
    def speaker_settings(self):
        if self.__speaker_settings is None:
            self.__speaker_settings = speaker.Settings(self.__sony_api)
        return self.__speaker_settings


class EqualizerSettings(object):

    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, method, **params):
        return self.__sony_api.send('audio', method, **params)

    @property
    def band_100hz(self):
        """
        Gets the 100 Hz equalizer band level.

        :return: 10 to -10 step of 1
        :rtype: int
        """
        return int(
            self.__send(
                'getCustomEqualizerSettings',
                target='100HzBandLevel'
            )[0][0]['currentValue']
        )

    @band_100hz.setter
    def band_100hz(self, value):
        """
        Sets the 100 Hz equalizer band.

        :param value: 10 to -10 step of 1
        :type value: int

        :return: None
        :rtype: None
        """
        self.__send(
            'setCustomEqualizerSettings',
            settings=[dict(target='100HzBandLevel', value=value)]
        )

    @property
    def band_330hz(self):
        """
        Gets the 330 Hz equalizer band level.

        :return: 10 to -10 step of 1
        :rtype: int
        """
        return int(
            self.__send(
                'getCustomEqualizerSettings',
                target='330HzBandLevel'
            )[0][0]['currentValue']
        )

    @band_330hz.setter
    def band_330hz(self, value):
        """
        Sets the 330 Hz equalizer band.

        :param value: 10 to -10 step of 1
        :type value: int

        :return: None
        :rtype: None
        """
        self.__send(
            'setCustomEqualizerSettings',
            settings=[dict(target='330HzBandLevel', value=value)]
        )

    @property
    def band_1000hz(self):
        """
        Gets the 1000 Hz equalizer band level.

        :return: 10 to -10 step of 1
        :rtype: int
        """
        return int(
            self.__send(
                'getCustomEqualizerSettings',
                target='1000HzBandLevel'
            )[0][0]['currentValue']
        )

    @band_1000hz.setter
    def band_1000hz(self, value):
        """
        Sets the 1000 Hz equalizer band.

        :param value: 10 to -10 step of 1
        :type value: int

        :return: None
        :rtype: None
        """
        self.__send(
            'setCustomEqualizerSettings',
            settings=[dict(target='1000HzBandLevel', value=value)]
        )

    @property
    def band_3300hz(self):
        """
        Gets the 3300 Hz equalizer band level.

        :return: 10 to -10 step of 1
        :rtype: int
        """
        return int(
            self.__send(
                'getCustomEqualizerSettings',
                target='3300HzBandLevel'
            )[0][0]['currentValue']
        )

    @band_3300hz.setter
    def band_3300hz(self, value):
        """
        Sets the 3300 Hz equalizer band.

        :param value: 10 to -10 step of 1
        :type value: int

        :return: None
        :rtype: None
        """
        self.__send(
            'setCustomEqualizerSettings',
            settings=[dict(target='3300HzBandLevel', value=value)]
        )

    @property
    def band_10000hz(self):
        """
        Gets the 10000 Hz equalizer band level.

        :return: 10 to -10 step of 1
        :rtype: int
        """
        return int(
            self.__send(
                'getCustomEqualizerSettings',
                target='10000HzBandLevel'
            )[0][0]['currentValue']
        )

    @band_10000hz.setter
    def band_10000hz(self, value):
        """
        Sets the 10000 Hz equalizer band.

        :param value: 10 to -10 step of 1
        :type value: int

        :return: None
        :rtype: None
        """
        self.__send(
            'setCustomEqualizerSettings',
            settings=[dict(target='10000HzBandLevel', value=value)]
        )

    @property
    def bass(self):
        """
        Gets the bass level.

        :return: 10 to -10 step of 1
        :rtype: int
        """
        return int(
            self.__send(
                'getCustomEqualizerSettings',
                target='bassLevel'
            )[0][0]['currentValue']
        )

    @bass.setter
    def bass(self, value):
        """
        Sets the bass level.

        :param value: 10 to -10 step of 1
        :type value: int

        :return: None
        :rtype: None
        """
        self.__send(
            'setCustomEqualizerSettings',
            settings=[dict(target='bassLevel', value=value)]
        )

    @property
    def treble(self):
        """
        Gets the treble level.

        :return: 10 to -10 step of 1
        :rtype: int
        """
        return int(
            self.__send(
                'getCustomEqualizerSettings',
                target='trebleLevel'
            )[0][0]['currentValue']
        )

    @treble.setter
    def treble(self, value):
        """
        Sets the treble level.

        :param value: 10 to -10 step of 1
        :type value: int

        :return: None
        :rtype: None
        """
        self.__send(
            'setCustomEqualizerSettings',
            settings=[dict(target='trebleLevel', value=value)]
        )
