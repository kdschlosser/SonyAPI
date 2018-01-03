# -*- coding: utf-8 -*-
#
# SonyAPI
# External control of Sony Bravia Generation 3 TV's
# Copyright (C) 2017  Kevin G. Schlosser
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


class Settings(object):

    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, method, **params):
        return self.__sony_api.send('audio', method, **params)

    @property
    def band_100hz(self):
        """
        100Hz equalizer band.

        **Getter:** Gets the 100Hz equalizer band level.

            *Returns:* ``10`` to ``-10`` step of ``1``

            *Return type:* `int`


        **Setter:** Sets the 100Hz equalizer band level.

            *Accepted values:* ``10`` to ``-10`` step of ``1``

            *Value type:* `int`
        """
        return int(
            self.__send(
                'getCustomEqualizerSettings',
                target='100HzBandLevel'
            )[0][0]['currentValue']
        )

    @band_100hz.setter
    def band_100hz(self, value):
        self.__send(
            'setCustomEqualizerSettings',
            settings=[dict(target='100HzBandLevel', value=value)]
        )

    @property
    def band_330hz(self):
        """
        330Hz equalizer band.

        **Getter:** Gets the 330Hz equalizer band level.

            *Returns:* ``10`` to ``-10`` step of ``1``

            *Return type:* `int`


        **Setter:** Sets the 330Hz equalizer band level.

            *Accepted values:* ``10`` to ``-10`` step of ``1``

            *Value type:* `int`
        """
        return int(
            self.__send(
                'getCustomEqualizerSettings',
                target='330HzBandLevel'
            )[0][0]['currentValue']
        )

    @band_330hz.setter
    def band_330hz(self, value):
        self.__send(
            'setCustomEqualizerSettings',
            settings=[dict(target='330HzBandLevel', value=value)]
        )

    @property
    def band_1000hz(self):
        """
        1000Hz equalizer band.

        **Getter:** Gets the 1000Hz equalizer band level.

            *Returns:* ``10`` to ``-10`` step of ``1``

            *Return type:* `int`


        **Setter:** Sets the 1000Hz equalizer band level.

            *Accepted values:* ``10`` to ``-10`` step of ``1``

            *Value type:* `int`
        """
        return int(
            self.__send(
                'getCustomEqualizerSettings',
                target='1000HzBandLevel'
            )[0][0]['currentValue']
        )

    @band_1000hz.setter
    def band_1000hz(self, value):
        self.__send(
            'setCustomEqualizerSettings',
            settings=[dict(target='1000HzBandLevel', value=value)]
        )

    @property
    def band_3300hz(self):
        """
        3300Hz equalizer band.

        **Getter:** Gets the 3300Hz equalizer band level.

            *Returns:* ``10`` to ``-10`` step of ``1``

            *Return type:* `int`


        **Setter:** Sets the 3300Hz equalizer band level.

            *Accepted values:* ``10`` to ``-10`` step of ``1``

            *Value type:* `int`
        """
        return int(
            self.__send(
                'getCustomEqualizerSettings',
                target='3300HzBandLevel'
            )[0][0]['currentValue']
        )

    @band_3300hz.setter
    def band_3300hz(self, value):
        self.__send(
            'setCustomEqualizerSettings',
            settings=[dict(target='3300HzBandLevel', value=value)]
        )

    @property
    def band_10000hz(self):
        """
        10000Hz equalizer band.

        **Getter:** Gets the 10000Hz equalizer band level.

            *Returns:* ``10`` to ``-10`` step of ``1``

            *Return type:* `int`


        **Setter:** Sets the 10000Hz equalizer band level.

            *Accepted values:* ``10`` to ``-10`` step of ``1``

            *Value type:* `int`
        """
        return int(
            self.__send(
                'getCustomEqualizerSettings',
                target='10000HzBandLevel'
            )[0][0]['currentValue']
        )

    @band_10000hz.setter
    def band_10000hz(self, value):
        self.__send(
            'setCustomEqualizerSettings',
            settings=[dict(target='10000HzBandLevel', value=value)]
        )

    @property
    def bass(self):
        """
        Bass.

        **Getter:** Gets the bass level.

            *Returns:* ``10`` to ``-10`` step of ``1``

            *Return type:* `int`


        **Setter:** Sets the bass level.

            *Accepted values:* ``10`` to ``-10`` step of ``1``

            *Value type:* `int`
        """
        return int(
            self.__send(
                'getCustomEqualizerSettings',
                target='bassLevel'
            )[0][0]['currentValue']
        )

    @bass.setter
    def bass(self, value):
        self.__send(
            'setCustomEqualizerSettings',
            settings=[dict(target='bassLevel', value=value)]
        )

    @property
    def treble(self):
        """
        Treble.

        **Getter:** Gets the treble level.

            *Returns:* ``10`` to ``-10`` step of ``1``

            *Return type:* `int`


        **Setter:** Sets the treble level.

            *Accepted values:* ``10`` to ``-10`` step of ``1``

            *Value type:* `int`
        """
        return int(
            self.__send(
                'getCustomEqualizerSettings',
                target='trebleLevel'
            )[0][0]['currentValue']
        )

    @treble.setter
    def treble(self, value):
        self.__send(
            'setCustomEqualizerSettings',
            settings=[dict(target='trebleLevel', value=value)]
        )
