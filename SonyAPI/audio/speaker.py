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
from ..exception import UnsupportedError


class SendBase(object):
    __key = ''

    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, target, **params):
        target = self.__key + target
        if params:
            params = dict(
                settings=[
                    dict(target=target, value=params['value'])
                ]
            )

            res = self.__sony_api.send(
                'audio',
                'getSpeakerSettings',
                target=target
            )[0][0]

            if res["isAvailable"]:
                self.__sony_api.send(
                    'audio',
                    'setSpeakerSettings',
                    **params
                )
            else:
                raise UnsupportedError

        else:
            res = self.__sony_api.send(
                'audio',
                'getSpeakerSettings',
                target=target
            )[0][0]

            if res['isAvailable']:
                return res['currentValue']
            else:
                raise UnsupportedError


class SpeakerBase(SendBase):

    @property
    def level(self):
        """
        Speaker level.

        **Getter:** Gets the Speaker level.

            *Returns:* ``-10.0`` (min) and ``10.0`` (max) with a step of ``0.5``

            *Return type:* `float`


        **Setter:** Sets the Speaker level.

            *Accepted values:* ``-10.0`` (min) and ``10.0`` (max) with a step of ``0.5``

            *Value type:* `float`
        """
        return float(self.__send('Level'))

    @level.setter
    def level(self, value):
        self.__send('Level', value=value)

    @property
    def distance(self):
        """
        Speaker distance (mm).

        **Getter:** Gets the Speaker distance.

            *Returns:* ``1000`` (min) and ``10000`` (max) with a step of ``10``

            *Return type:* `int`


        **Setter:** Sets the Speaker distance.

            *Accepted values:* ``1000`` (min) and ``10000`` (max) with a step of ``10``

            *Value type:* `int`
        """
        return self.__send('DistanceMM')

    @distance.setter
    def distance(self, value):
        self.__send('DistanceMM', value=value)


class PositionBase(SendBase):

    def __verify_position_type(self):
        if self.__key not in ('front', 'frontHigh', 'center', 'surround'):
            raise AttributeError

    @property
    def bass(self):
        """
        Bass.

        **Getter:** Gets the Speaker bass level.

            *Returns:* ``-10`` (min) and ``10`` (max) with a step of ``1``

            *Return type:* `int`


        **Setter:** Sets the Speaker bass level.

            *Accepted values:* ``-10`` (min) and ``10`` (max) with a step of ``1``

            *Value type:* `int`
        """
        self.__verify_position_type()

        return int(
            self.__sony_api.send(
                'audio',
                'getCustomEqualizerSettings',
                target=self.__key + 'BassLevel'
            )[0][0]['currentValue']
        )

    @bass.setter
    def bass(self, value):
        self.__verify_position_type()

        self.__sony_api.send(
            'audio',
            'setCustomEqualizerSettings',
            settings=[dict(target=self.__key + 'BassLevel', value=value)]
        )

    @property
    def treble(self):
        """
        Treble.

        **Getter:** Gets the Speaker treble level.

            *Returns:* ``-10`` (min) and ``10`` (max) with a step of ``1``

            *Return type:* `int`


        **Setter:** Sets the Speaker treble level.

            *Accepted values:* ``-10`` (min) and ``10`` (max) with a step of ``1``

            *Value type:* `int`
        """
        self.__verify_position_type()

        return int(
            self.__sony_api.send(
                'audio',
                'getCustomEqualizerSettings',
                target=self.__key + 'TrebleLevel'
            )[0][0]['currentValue']
        )

    @treble.setter
    def treble(self, value):
        self.__verify_position_type()

        self.__sony_api.send(
            'audio',
            'setCustomEqualizerSettings',
            settings=[dict(target=self.__key + 'TrebleLevel', value=value)]
        )

    @property
    def size(self):
        """
        Speaker size.

        **Getter:** Gets the Speaker size.

            *Returns:*

                * ``"large"`` - Large size speaker.

                    If you connect large speakers that will effectively
                    reproduce bass frequencies, select this.

                * ``"small"`` - Small size speaker.

                    If the sound is distorted, or you hear a lack of surround
                    effects when using multi channel surround

            *Return type:* `str`

        **Setter:** Sets the Speaker size.

            *Accepted values:*

                * ``"large"`` - Large size speaker.

                    If you connect large speakers that will effectively
                    reproduce bass frequencies, select this.

                * ``"small"`` - Small size speaker.

                    If the sound is distorted, or you hear a lack of surround
                    effects when using multi channel surround sound, select
                    this.

            *Value type:* `str`
        """
        return self.__send('Size')

    @size.setter
    def size(self, value):
        self.__send('Size', value=value)

    @property
    def crossover_frequency(self):
        """
        Crossover frequency (Hz).

        **Getter:** Gets the Crossover frequency.

            *Returns:* ``40`` (min) and ``200`` (max) with a step of ``10``

            *Return type:* `int`


        **Setter:** Sets the Crossover frequency.

            *Accepted values:* ``40`` (min) and ``200`` (max) with a step of ``10``

            *Value type:* `int`
        """
        return self.__send('CrossoverFreq')

    @crossover_frequency.setter
    def crossover_frequency(self, value):
        self.__send('CrossoverFreq', value=value)


class FrontLeft(SpeakerBase):
    __key = 'frontL'


class FrontRight(SpeakerBase):
    __key = 'frontR'


class SurroundLeft(SpeakerBase):
    __key = 'surroundL'


class SurroundRight(SpeakerBase):
    __key = 'surroundR'


class SurroundBackLeft(SpeakerBase):
    __key = 'surroundBackL'


class SurroundBackRight(SpeakerBase):
    __key = 'surroundBackR'


class FrontHighLeft(SpeakerBase):
    __key = 'frontHighL'


class FrontHighRight(SpeakerBase):
    __key = 'frontHighR'


class FrontHigh(PositionBase):
    __key = 'frontHigh'

    def __init__(self, sony_api):
        PositionBase.__init__(self, sony_api)
        self.__left = None
        self.__right = None

    @property
    def left(self):
        """
        Front High Left settings.

        *Returns:* `FrontHighLeft` instance

        *Return type:* `FrontHighLeft`
        """
        if self.__left is None:
            self.__left = FrontHighLeft(self.__sony_api)
        return self.__left

    @property
    def right(self):
        """
        Front High Right settings.

        *Returns:* `FrontHighRight` instance

        *Return type:* `FrontHighRight`
        """
        if self.__right is None:
            self.__right = FrontHighRight(self.__sony_api)
        return self.__right


class Front(PositionBase):
    __key = 'front'

    def __init__(self, sony_api):
        PositionBase.__init__(self, sony_api)
        self.__left = None
        self.__right = None
        self.__high = None
        self.__center = None

    @property
    def left(self):
        """
        Front Left settings.

        *Returns:* `FrontLeft` instance

        *Return type:* `FrontLeft`
        """
        if self.__left is None:
            self.__left = FrontLeft(self.__sony_api)
        return self.__left

    @property
    def right(self):
        """
        Front Right settings.

        *Returns:* `SonyAPI.audio.speaker.FrontRight` instance

        *Return type:* `SonyAPI.audio.speaker.FrontRight`
        """
        if self.__right is None:
            self.__right = FrontRight(self.__sony_api)
        return self.__right

    @property
    def center(self):
        """
        Center settings.

        *Returns:* `SonyAPI.audio.speaker.Center` instance

        *Return type:* `SonyAPI.audio.speaker.Center`
        """
        if self.__right is None:
            self.__right = Center(self.__sony_api)
        return self.__right

    @property
    def high(self):
        """
        Front High settings.

        *Returns:* `SonyAPI.audio.speaker.FrontHigh` instance

        *Return type:* `SonyAPI.audio.speaker.FrontHigh`
        """
        if self.__right is None:
            self.__right = FrontHigh(self.__sony_api)
        return self.__right

    @property
    def speaker_position(self):
        """
        Speaker location.

        **Getter:** Gets the Speaker location.

            *Returns:*

                * ``"floor"`` - Speaker position is Floor speaker.
                * ``"inCeiling"`` - Speaker position is In-Ceiling speaker.

            *Return type:* `str`

        **Setter:** Sets the Speaker location.

            *Accepted values:*

                * ``"floor"`` - Speaker position is Floor speaker.
                * ``"inCeiling"`` - Speaker position is In-Ceiling speaker.

            *Value type:* `str`
        """
        self.__key = ''
        try:
            return self.__send('speakerPosition')
        finally:
            self.__key = 'front'

    @speaker_position.setter
    def speaker_position(self, value):
        self.__key = ''
        self.__send('speakerPosition', value=value)
        self.__key = 'front'

    @property
    def ceiling_height(self):
        """
        Speaker height (mm).

        **Getter:** Gets the Speaker height.

            *Returns:* ``2000`` (min) and ``10000`` (max) with a step of ``10``

            *Return type:* `int`


        **Setter:** Sets the Speaker height.

            *Accepted values:* ``2000`` (min) and ``10000`` (max) with a step of ``10``

            *Value type:* `int`
        """
        self.__key = ''
        try:
            return self.__send('ceilingSpeakerHeight')
        finally:
            self.__key = 'front'

    @ceiling_height.setter
    def ceiling_height(self, value):
        self.__key = ''
        self.__send('ceilingSpeakerHeight', value=value)
        self.__key = 'front'

    @property
    def in_ceiling_speaker_mode(self):
        """
        In ceiling speaker mode.

        In a setup where the front and center speakers are installed in the
        ceiling, lowering the audio output position to the screen height allows
        you to enjoy a more natural experience.

        **Getter:** Gets the In ceiling speaker mode.

            *Returns:*

                * ``True`` - In Ceiling Speaker Mode is enabled.
                * ``False`` - In Ceiling Speaker Mode is disabled.

            *Return type:* `bool`

        **Setter:** Sets the In ceiling speaker mode.

            *Accepted values:*

                * ``True`` - Enable In Ceiling Speaker Mode.
                * ``False`` - Disable In Ceiling Speaker Mode.

            *Value type:* `bool`
        """
        self.__key = ''
        try:
            return (
                True if self.__send('inCeilingSpeakerMode') == 'on' else False
            )
        finally:
                self.__key = 'front'

    @in_ceiling_speaker_mode.setter
    def in_ceiling_speaker_mode(self, value):
        self.__key = ''
        self.__send('inCeilingSpeakerMode', value='on' if value else 'off')
        self.__key = 'front'


class SurroundBack(SpeakerBase):
    __key = 'surroundBack'

    def __init__(self, sony_api):
        SpeakerBase.__init__(self, sony_api)
        self.__left = None
        self.__right = None

    @property
    def left(self):
        """
        Surround Back Left settings.

        *Returns:* `SonyAPI.audio.speaker.SurroundBackLeft` instance

        *Return type:* `SonyAPI.audio.speaker.SurroundBackLeft`
        """
        if self.__left is None:
            self.__left = SurroundBackLeft(self.__sony_api)
        return self.__left

    @property
    def right(self):
        """
        Surround Back Right settings.

        *Returns:* `SonyAPI.audio.speaker.SurroundBackRight` instance

        *Return type:* `SonyAPI.audio.speaker.SurroundBackRight`
        """
        if self.__right is None:
            self.__right = SurroundBackRight(self.__sony_api)
        return self.__right

    @property
    def zone_assignment(self):
        """
        Speaker assignment.

        **Getter:** Gets the Speaker assignment.

            *Returns:*

                * ``"zone2"`` - Surround back speaker is assigned for Zone 2.

                    When using the Zone 2 connection.

                * ``"biAmp"`` - Surround back speaker is assigned for Bi-Amp.

                    When using the bi-amplifier connection.

                * ``"frontB"`` - Surround back speaker is assigned for Front B.

                    When using the front B speaker connection.

                * ``"off"`` - When none of the connections above are used.

            *Return type:* `str`

        **Setter:** Sets the Speaker assignment.

            *Accepted values:*

                * ``"zone2"`` - Surround back speaker is assigned for Zone 2.

                    When using the Zone 2 connection.

                * ``"biAmp"`` - Surround back speaker is assigned for Bi-Amp.

                    When using the bi-amplifier connection.

                * ``"frontB"`` - Surround back speaker is assigned for Front B.

                    When using the front B speaker connection.

                * ``"off"`` - When none of the connections above are used.

            *Value type:* `str`
        """

        return self.__send('SpeakerAssign')

    @zone_assignment.setter
    def zone_assignment(self, value):
        self.__send('SpeakerAssign', value=value)


class Surround(PositionBase, SpeakerBase):
    __key = 'surround'

    def __init__(self, sony_api):
        PositionBase.__init__(self, sony_api)
        SpeakerBase.__init__(self, sony_api)
        self.__left = None
        self.__right = None
        self.__back = None

    @property
    def left(self):
        """
        Surround Left settings.

        *Returns:* `SonyAPI.audio.speaker.SurroundLeft` instance

        *Return type:* `SonyAPI.audio.speaker.SurroundLeft`
        """
        if self.__left is None:
            self.__left = SurroundLeft(self.__sony_api)
        return self.__left

    @property
    def right(self):
        """
        Surround Right settings.

        *Returns:* `SonyAPI.audio.speaker.SurroundRight` instance

        *Return type:* `SonyAPI.audio.speaker.SurroundRight`
        """
        if self.__right is None:
            self.__right = SurroundRight(self.__sony_api)
        return self.__right

    @property
    def back(self):
        """
        Surround Back settings.

        *Returns:* `SonyAPI.audio.speaker.SurroundBack` instance

        *Return type:* `SonyAPI.audio.speaker.SurroundBack`
        """
        if self.__back is None:
            self.__back = SurroundBack(self.__sony_api)
        return self.__back

    @property
    def zone_assignment(self):
        """
        Speaker assignment.

        **Getter:** Gets the Speaker assignment.

            *Returns:*

                * ``"zone3"`` - Surround speaker is assigned for Zone 3.
                * ``"off"`` - Surround speaker is not assigned for Zone 3.

            *Return type:* `str`

        **Setter:** Sets the Speaker assignment.

            *Accepted values:*

                * ``"zone3"`` - Surround speaker is assigned for Zone 3.
                * ``"off"`` - Surround speaker is not assigned for Zone 3.

            *Value type:* `str`
        """
        return self.__send('SpeakerAssign')

    @zone_assignment.setter
    def zone_assignment(self, value):
        self.__send('SpeakerAssign', value=value)


class Subwoofer(PositionBase, SpeakerBase):
    __key = 'subwoofer'

    def __init__(self, sony_api):
        PositionBase.__init__(self, sony_api)
        SpeakerBase.__init__(self, sony_api)

    @property
    def level(self):
        """
        Speaker level.

        Note that the range and step values vary depending on device.

        **Getter:** Gets the Speaker level.

            *Returns:* ``0`` (min) and ``24`` (max) with a step of ``1``

            *Return type:* `int`


        **Setter:** Sets the Speaker level.

            *Accepted values:* ``0`` (min) and ``24`` (max) with a step of ``1``

            *Value type:* `int`
        """

        return self.__send('Level')

    @level.setter
    def level(self, value):
        self.__send('Level', value=value)

    @property
    def crossover_frequency(self):
        """
        Crossover frequency (Hz).

        All frequencies below the cut off frequency are output to the Wireless
        Subwoofer instead of the TV speakers.

        **Getter:** Gets the Crossover frequency.

            *Returns:* ``0`` (min) and ``30`` (max) with a step of ``1``

            *Return type:* `int`


        **Setter:** Sets the Crossover frequency.

            *Accepted values:* ``0`` (min) and ``30`` (max) with a step of ``1``

            *Value type:* `int`
        """
        return self.__send('Freq')

    @crossover_frequency.setter
    def crossover_frequency(self, value):
        self.__send('Freq', value=value)

    @property
    def phase(self):
        """
        Phase polarity.

        **Getter:** Gets the Phase polarity.

            *Returns:*

                * ``"normal"`` - Normal phase.
                * ``"reverse"`` - Reverse phase.

            *Return type:* `str`

        **Setter:** Sets the Phase polarity.

            *Accepted values:*

                * ``"normal"`` - Normal phase.
                * ``"reverse"`` - Reverse phase.

            *Value type:* `str`
        """
        return self.__send('Phase')

    @phase.setter
    def phase(self, value):
        self.__send('Phase', value=value)

    @property
    def power(self):
        """
        Power.

        **Getter:** Gets the power state.

            *Returns:*

                * ``True`` - Subwoofer is on.
                * ``False`` - Subwoofer is off.

            *Return type:* `bool`

        **Setter:** Sets the power state.

            *Accepted values:*

                * ``True`` - Subwoofer on.
                * ``False`` - Subwoofer off.

            *Value type:* `bool`
        """
        return self.__send('Power') == "on"

    @power.setter
    def power(self, value):
        self.__send('Power', value='on' if value else 'off')

    @property
    def low_pass_filter(self):
        """
        Low pass filter.

        The low-pass filter works when PCM signals are input via an all
        connection. Turn the function on if connecting a subwoofer without
        the crossover frequency function.

        **Getter:** Gets the Low pass filter state.

            *Returns:*

                * ``True`` - Low pass filter is enabled.
                * ``False`` - Low pass filter is disabled.

            *Return type:* `bool`

        **Setter:** Sets the Low pass filter state.

            *Accepted values:*

                * ``True`` - Low pass filter enabled.
                * ``False`` - Low pass filter disabled.

            *Value type:* `bool`
        """
        return self.__send('Lpf') == 'on'

    @low_pass_filter.setter
    def low_pass_filter(self, value):
        self.__send('Lpf', value='on' if value else 'off')

    @property
    def hdmi_pcm_level(self):
        """
        PCM level.

        The level for each input to which an HDMI input jack is assigned can
        be set independently. 0 dB or +10 dB when PCM signals are input via an
        HDMI connection.

        **Getter:** Gets the PCM level.

            *Returns:*

                * ``"auto"`` - Automatically sets the level to 0 dB or +10 dB.

                    Depends on the audio stream.

                * ``"10db"`` - Speaker Level is set to +10 dB.
                * ``"0db"`` - Speaker Level is set to 0 dB.

            *Return type:* `str`

        **Setter:** Sets the PCM level.

            *Accepted values:*

                * ``"auto"`` - Automatically sets the level to 0 dB or +10 dB.

                    Depends on the audio stream.

                * ``"10db"`` - Speaker Level is set to +10 dB.
                * ``"0db"`` - Speaker Level is set to 0 dB.

            *Value type:* `str`
        """
        return self.__send('LevelHdmiPcm')

    @hdmi_pcm_level.setter
    def hdmi_pcm_level(self, value):
        self.__send('LevelHdmiPcm', value=value)


class Center(PositionBase, SpeakerBase):
    __key = 'center'

    def __init__(self, sony_api):
        PositionBase.__init__(self, sony_api)
        SpeakerBase.__init__(self, sony_api)

    @property
    def up_lift(self):
        """
        Uplift level.

        **Getter:** Gets the Uplift level.

            *Returns:* ``0`` (min) and ``10`` (max) with a step of ``1``

            *Return type:* `int`


        **Setter:** Sets the Uplift level.

            *Accepted values:* ``0`` (min) and ``10`` (max) with a step of ``1``

            *Value type:* `int`
        """
        value = self.__send('LiftUp')

        if value == 'off':
            value = 0

        return value

    @up_lift.setter
    def up_lift(self, value):
        self.__send('LiftUp', value=value if value else 'off')


class Settings(object):
    __key = ''
    def __init__(self, sony_api):
        self.__sony_api = sony_api

        self.__front = None
        self.__surround = None
        self.__subwoofer = None

    def __send(self, *args, **kwargs):
        return self.__sony_api.send(self, *args, **kwargs)

    @property
    def front(self):
        """
        Front speaker settings.

        *Returns:* `SonyAPI.audio.speaker.Front` instance

        *Return type:* `SonyAPI.audio.speaker.Front`
        """
        if self.__front is None:
            self.__front = Front(self.__sony_api)
        return self.__front

    @property
    def surround(self):
        """
        Front speaker settings.

        *Returns:* `SonyAPI.audio.speaker.Surround` instance

        *Return type:* `SonyAPI.audio.speaker.Surround`
        """
        if self.__surround is None:
            self.__surround = Surround(self.__sony_api)
        return self.__surround

    @property
    def subwoofer(self):
        """
        Subwoofer speaker settings.

        *Returns:* `SonyAPI.audio.speaker.Subwoofer` instance

        *Return type:* `SonyAPI.audio.speaker.Subwoofer`
        """
        if self.__subwoofer is None:
            self.__subwoofer = Subwoofer(self.__sony_api)
        return self.__subwoofer


    @property
    def tv_position(self):
        """
        TV position.

        **Getter:** Gets the TV position.

            *Returns:*

                * ``"tableTop"`` - Provides the best sound quality when you place the TV on a TV stand.
                * ``"wallMount"`` - Provides the best sound quality when you hang the TV on a wall.

            *Return type:* `str`

        **Setter:** Sets the TV position.

            *Accepted values:*

                * ``"tableTop"`` - Provides the best sound quality when you place the TV on a TV stand.
                * ``"wallMount"`` - Provides the best sound quality when you hang the TV on a wall.

            *Value type:* `str`
        """
        return self.__send('tvPosition')

    @tv_position.setter
    def tv_position(self, value):
        self.__send('tvPosition', value=value)

    @property
    def speaker_selection(self):
        """
        Front speaker output selection.

        **Getter:** Gets the Front speaker output selection.

            *Returns:*

                * ``"speakerA"`` - Speaker A.

                    Speakers connected to the SPEAKERS FRONT A terminals.

                * ``"speakerB"`` - Speaker B.

                    Speakers connected to the
                    SPEAKERS SURROUND BACK/BI-AMP/FRONT HIGH/FRONT B terminals.

                * ``"speakerA_B"`` - Speaker A and Speaker B.

                    Speakers connected to both the SPEAKERS FRONT A and
                    SPEAKERS SURROUND BACK/BIAMP/FRONT HIGH/FRONT B terminals
                    (parallel connection).

                * ``"off"`` - No audio signals are output from any speaker terminals.

            *Return type:* `str`

        **Setter:** Sets the Front speaker output selection.

            *Accepted values:*

                * ``"speakerA"`` - Speaker A.

                    Speakers connected to the SPEAKERS FRONT A terminals.

                * ``"speakerB"`` - Speaker B.

                    Speakers connected to the
                    SPEAKERS SURROUND BACK/BI-AMP/FRONT HIGH/FRONT B terminals.

                * ``"speakerA_B"`` - Speaker A and Speaker B.

                    Speakers connected to both the SPEAKERS FRONT A and
                    SPEAKERS SURROUND BACK/BIAMP/FRONT HIGH/FRONT B terminals
                    (parallel connection).

                * ``"off"`` - No audio signals are output from any speaker terminals.

            *Value type:* `str`
        """
        return self.__send('speakerSelection')

    @speaker_selection.setter
    def speaker_selection(self, value):
        self.__send('speakerSelection', value=value)

    @property
    def distance_unit(self):
        """
        Distance Unit. (ft, mm)

        **Getter:** Gets the Distance Unit.

            *Returns:*

                * ``"meter"`` - The distance is displayed in meters.
                * ``"feet"`` - The distance is displayed in feet.

            *Return type:* `str`

        **Setter:** Sets the Distance Unit.

            *Accepted values:*

                * ``"meter"`` - The distance is displayed in meters.
                * ``"feet"`` - The distance is displayed in feet.

            *Value type:* `str`
        """
        return self.__send('distanceUnit')

    @distance_unit.setter
    def distance_unit(self, value):
        self.__send('distanceUnit', value=value)

    @property
    def speaker_pattern(self):
        """
        Speaker pattern.

        **Getter:** Gets the Speaker pattern.

            *Returns:*

                * ``"2_0_0"`` - Speaker pattern is 2/0
                * ``"2_0_1"`` - Speaker pattern is 2/0.1
                * ``"3_0_0"`` - Speaker pattern is 3/0
                * ``"3_0_1"`` - Speaker pattern is 3/0.1
                * ``"2_2_0"`` - Speaker pattern is 2/2
                * ``"2_2_1"`` - Speaker pattern is 2/2.1
                * ``"3_2_0"`` - Speaker pattern is 3/2
                * ``"3_2_1"`` - Speaker pattern is 3/2.1
                * ``"2_3_0"`` - Speaker pattern is 2/3
                * ``"2_3_1"`` - Speaker pattern is 2/3.1
                * ``"3_3_0"`` - Speaker pattern is 3/3
                * ``"3_3_1"`` - Speaker pattern is 3/3.1
                * ``"2_4_0"`` - Speaker pattern is 2/4
                * ``"2_4_1"`` - Speaker pattern is 2/4.1
                * ``"3_4_0"`` - Speaker pattern is 3/4
                * ``"3_4_1"`` - Speaker pattern is 3/4.1
                * ``"4_2_0"`` - Speaker pattern is 4/2
                * ``"4_2_1"`` - Speaker pattern is 4/2.1
                * ``"5_2_0"`` - Speaker pattern is 5/2
                * ``"5_2_1"`` - Speaker pattern is 5/2.1

            *Return type:* `str`

        **Setter:** Sets the Speaker pattern.

            *Accepted values:*

                * ``"2_0_0"`` - Speaker pattern is 2/0
                * ``"2_0_1"`` - Speaker pattern is 2/0.1
                * ``"3_0_0"`` - Speaker pattern is 3/0
                * ``"3_0_1"`` - Speaker pattern is 3/0.1
                * ``"2_2_0"`` - Speaker pattern is 2/2
                * ``"2_2_1"`` - Speaker pattern is 2/2.1
                * ``"3_2_0"`` - Speaker pattern is 3/2
                * ``"3_2_1"`` - Speaker pattern is 3/2.1
                * ``"2_3_0"`` - Speaker pattern is 2/3
                * ``"2_3_1"`` - Speaker pattern is 2/3.1
                * ``"3_3_0"`` - Speaker pattern is 3/3
                * ``"3_3_1"`` - Speaker pattern is 3/3.1
                * ``"2_4_0"`` - Speaker pattern is 2/4
                * ``"2_4_1"`` - Speaker pattern is 2/4.1
                * ``"3_4_0"`` - Speaker pattern is 3/4
                * ``"3_4_1"`` - Speaker pattern is 3/4.1
                * ``"4_2_0"`` - Speaker pattern is 4/2
                * ``"4_2_1"`` - Speaker pattern is 4/2.1
                * ``"5_2_0"`` - Speaker pattern is 5/2
                * ``"5_2_1"`` - Speaker pattern is 5/2.1

            *Value type:* `str`
        """
        return self.__send('speakerPattern')

    @speaker_pattern.setter
    def speaker_pattern(self, value):
        self.__send('speakerPattern', value=value)
