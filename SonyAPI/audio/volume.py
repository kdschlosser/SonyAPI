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


from __future__ import absolute_import

from ..api_const import PY2


class VolumeItem(object):
    """
    Volume control point.

    This class represents a volume control point on the device.

    **Operators:**

            >>> sony_api.audio.volume.speaker = 10

        ``>``: *Volume greater then other.*

            >>> sony_api.audio.volume.speaker > 10
            False

        ``>=``: *Volume greater then or equal to other.*

            >>> sony_api.audio.volume.speaker >= 10
            True

        ``<``: *Volume less then other.*

            >>> sony_api.audio.volume.speaker < 10
            False

        ``<=``: *Volume less then or equal to other.*

            >>> sony_api.audio.volume.speaker <= 10
            True

        ``==``: *Volume equal to other.*

            >>> sony_api.audio.volume.speaker == 10
            True

        ``!=``: *Volume not equal to other.*

            >>> sony_api.audio.volume.speaker != 10
            False

        ``+``: *Other added to volume and volume added to other.*

            >>> sony_api.audio.volume.speaker + 1
            11

            >>> 1 + sony_api.audio.volume.speaker
            11

        ``+=``: *Other added to volume and sets value.*

            >>> sony_api.audio.volume.speaker += 1
            >>> int(sony_api.audio.volume.speaker)
            11

        ``-``: *Other subtracted from volume and volume subtracted from other.*

            >>> sony_api.audio.volume.speaker - 1
            9

            >>> 1 - sony_api.audio.volume.speaker
            -9

        ``-=``: *Other subtracted from volume and sets value.*

            >>> sony_api.audio.volume.speaker -= 1
            >>> int(sony_api.audio.volume.speaker)
            9

        ``*``: *Volume multiplied by other and other multiplied by volume.*

            >>> sony_api.audio.volume.speaker * 2
            20

            >>> 2 * sony_api.audio.volume.speaker
            20

        ``*=``: *Volume multiplied by other and sets value.*

            >>> sony_api.audio.volume.speaker *= 2
            >>> int(sony_api.audio.volume.speaker)
            20

        ``/``: *Volume divided by other and other divided by volume.*

            >>> sony_api.audio.volume.speaker / 2
            5

            >>> 50 / sony_api.audio.volume.speaker
            5

        ``/=``: *Volume divided by other and sets value.*

            >>> sony_api.audio.volume.speaker /= 2
            >>> int(sony_api.audio.volume.speaker)
            5


    **Type conversions:**

        ``float(self)``:

            >>> float(sony_api.audio.volume.speaker)
            10.0

        ``int(self)``:

            >>> int(sony_api.audio.volume.speaker)
            10

        ``str(self)``:

            >>> str(sony_api.audio.volume.speaker)
            "10"

        ``unicode(self)``:

            >>> unicode(sony_api.audio.volume.speaker)
            u\'10\'


    """

    # noinspection PyPep8Naming
    def __init__(
        self,
        sony_api,
        minVolume=0,
        maxVolume=0,
        **kwargs
    ):
        self.__sony_api = sony_api

        if 'target' in kwargs:
            self.__target = kwargs['target']
            self.__output = None
        else:
            self.__output = kwargs['output']
            self.__target = None

        self.min_volume = int(minVolume)
        self.max_volume = int(maxVolume)

    def __set_volume(self, value):
        volume = int(value)
        if volume < self.min_volume:
            volume = self.min_volume

        if volume > self.max_volume:
            volume = self.max_volume

        if self.__target is None:
            params = dict(output=self.__output)
        else:
            params = dict(target=self.__target)

        self.__sony_api.send(
            'audio',
            'setAudioVolume',
            volume=str(volume),
            **params
        )

    def __send(self, method, **params):
        return self.__sony_api('audio', method, **params)

    @property
    def __volume_info(self):
        if self.__target is None:
            target = dict(output=self.__output)
        else:
            target = dict(target=self.__target)

        return self.__send('getVolumeInformation', **target)[0][0]

    def up(self):
        """
        Volume up.
        """
        self.__set_volume(self + 1)

    def down(self):
        """
        Volume down.
        """
        self.__set_volume(self - 1)

    @property
    def mute(self):
        """
        Mute state.

        **Getter:** Gets the current mute state.

            *Returns:*

                * ``True`` - Mute is on.
                * ``False`` - Mute is off.

            *Return type:* `bool`

                >>> sony_api.audio.volume.speaker.mute
                True

        **Setter:** Sets the mute state.

            *Accepted values:*

                * ``True`` - Mute is on.
                * ``False`` - Mute is off.

            *Value type:* `bool`

                >>> sony_api.audio.volume.speaker.mute = False


        """
        return self.__volume_info['mute'] in ('on', True)

    @mute.setter
    def mute(self, value):
        if not isinstance(self.__volume_info['mute'], bool):
            params = dict(
                mute='on' if value else 'off'
            )
        else:
            params = dict(status=value)

        self.__send('setAudioMute', **params)

    def toggle_mute(self):
        """
        Toggle the mute state.
        """
        self.mute = not self.mute

    def __lt__(self, other):
        return int(self.__volume_info['volume']) < int(other)

    def __le__(self, other):
        return int(self.__volume_info['volume']) <= int(other)

    def __eq__(self, other):
        return int(self.__volume_info['volume']) == int(other)

    def __ne__(self, other):
        return int(self.__volume_info['volume']) != int(other)

    def __gt__(self, other):
        return int(self.__volume_info['volume']) > int(other)

    def __ge__(self, other):
        return int(self.__volume_info['volume']) >= int(other)

    def __add__(self, other):
        return int(self.__volume_info['volume']) + int(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return other - int(self.__volume_info['volume'])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rdiv__(self, other):
        return other / int(self.__volume_info['volume'])

    def __sub__(self, other):
        return int(self.__volume_info['volume']) - int(other)

    def __mul__(self, other):
        return int(self.__volume_info['volume']) * int(other)

    def __div__(self, other):
        return int(self.__volume_info['volume']) / int(other)

    def __iadd__(self, other):
        self.__set_volume(int(self.__volume_info['volume']) + int(other))
        return self

    def __isub__(self, other):
        self.__set_volume(int(self.__volume_info['volume']) - int(other))
        return self

    def __imul__(self, other):
        self.__set_volume(int(self.__volume_info['volume']) * int(other))
        return self

    def __idiv__(self, other):
        self.__set_volume(int(self.__volume_info['volume']) / int(other))
        return self

    def __float__(self):
        return float(int(self.__volume_info['volume']))

    def __int__(self):
        return int(self.__volume_info['volume'])

    def __str__(self):
        return str(int(self.__volume_info['volume']))

    if PY2:
        def __unicode__(self):
            return unicode(str(self))


class OutputItem(object):
    """
    Audio device volume control point handler.

    This class dynamically builds a volume control point that is associated
    with an audio device. The reason this is done dynamically is that not all
    devices share the same control points.

    *Example:*

        We want to access the zone 1 output.

            >>> sony_api.audio.volume.extOutput.zone1

    *Returned value:*

        `SonyAPI.audio.volume.VolumeItem` instance
    """

    def __init__(self, sony_api, name):
        self.__sony_api = sony_api
        self.__name__ = ''
        for item in name.split('_'):
            self.__name__ += item[0].upper() + item[1:]

        self.__name = name.replace('_', '-')

    def __send(self, method, **params):
        return self.__sony_api.send('audio', method, **params)

    @property
    def name(self):
        return self.__name

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        for device in self.__send('getVolumeInformation')[0]:
            if 'output' in device and device['output'].startswith(self.name):
                split_output = device['output'].split('?')
                if len(split_output) == 1:
                    attr_name = split_output[0].split(':')[1]
                else:
                    attr_name = split_output[1].replace('=', '')

                if attr_name == item:
                    self.__dict__[item] = attr = VolumeItem(
                        self.__sony_api,
                        **device
                    )
                    return attr
        raise AttributeError

    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        else:
            control_point = getattr(self, key)
            if value < int(control_point):
                control_point -= value
            elif value > int(control_point):
                control_point += value


class Volume(object):
    """
    Volume control point handler.

    This class dynamically builds a volume control point that is associated
    with a device. The reason this is done dynamically is that not all devices
    share the same control points.

    Example:

        **TV's:**

            ``volume.speaker``

            ``volume.headphones``

            *Returned value:*

                `SonyAPI.audio.volume.VolumeItem` instance


        **AVR's:**

            ``volume.extOutput``

            *Returned value:*

                `SonyAPI.audio.volume.OutputItem` instance


    """
    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, method, **params):
        return self.__sony_api.send('audio', method, **params)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        for device in self.__send('getVolumeInformation')[0]:
            if "target" in device and device['target'] == item:
                self.__dict__[item] = attr = VolumeItem(
                    self.__sony_api,
                    **device
                )
                return attr
            if (
                'output' in device and
                device['output'].startswith(item.replace('_', '-'))
            ):
                self.__dict__[item] = attr = OutputItem(self.__sony_api, item)
                return attr

        raise AttributeError

    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        else:
            control_point = getattr(self, key)
            if isinstance(control_point, VolumeItem):
                if value < int(control_point):
                    control_point -= value
                elif value > int(control_point):
                    control_point += value
            else:
                raise AttributeError

