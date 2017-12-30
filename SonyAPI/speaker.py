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


from exception import UnsupportedError


class SendBase(object):
    _key = ''

    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, target, **params):
        target = self._key + target
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
        Gets the level of a speaker.

        :return: Returned values will be between -10.0 (min) and 10.0 (max)
            with a step of 0.5
        :rtype: float
        """
        return float(self.__send('Level'))

    @level.setter
    def level(self, value):
        """
        Sets the level of a speaker.

        :param value: values will be between -10.0 (min) and 10.0 (max)
            with a step of 0.5.
        :type value: float
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self.__send('Level', value=value)

    @property
    def distance(self):
        """
        Gets the distance of a speaker.

        (Unit: mm)

        :return: Returned values will be between 1000 (min) and 10000 (max)
            with a step of 10
        :rtype: int
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        return self.__send('DistanceMM')

    @distance.setter
    def distance(self, value):
        """
        Sets the  distance of a speaker.

        (Unit: mm)

        :param value: values will be between 1000 (min) and 10000 (max)
            with a step of 10.
        :type value: int
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self.__send('DistanceMM', value=value)


class PositionBase(SendBase):

    @property
    def size(self):
        """
        Gets the Size of speakers.

        :return: Returned values will be one of the following:
            "large" - Large size speaker. If you connect large speakers that
            will effectively reproduce bass frequencies, select this.
            "small" - Small size speaker. If the sound is distorted, or you
            hear a lack of surround effects when using multi channel surround
            sound, select this.

        :rtype: str
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        return self.__send('Size')

    @size.setter
    def size(self, value):
        """
        Sets the Size of speakers.

        :param value: One of the following:
            "large" - Large size speaker. If you connect large speakers that
            will effectively reproduce bass frequencies, select this.
            "small" - Small size speaker. If the sound is distorted, or you
            hear a lack of surround effects when using multi channel surround
            sound, select this.
        :type value: str
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self.__send('Size', value=value)

    @property
    def crossover_frequency(self):
        """
        Gets the crossover frequency of speakers. (Hz)

        :return: Returned values will be between 40 (min) and 200 (max)
            with a step of 10.
        :rtype: int
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        return self.__send('CrossoverFreq')

    @crossover_frequency.setter
    def crossover_frequency(self, value):
        """
        Sets the crossover frequency of speakers. (Hz)

        :param value: values will be between 40 (min) and 200 (max)
            with a step of 10.
        :type value: int
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self.__send('CrossoverFreq', value=value)


class FrontLeft(SpeakerBase):
    _key = 'frontL'


class FrontRight(SpeakerBase):
    _key = 'frontR'


class SurroundLeft(SpeakerBase):
    _key = 'surroundL'


class SurroundRight(SpeakerBase):
    _key = 'surroundR'


class SurroundBackLeft(SpeakerBase):
    _key = 'surroundBackL'


class SurroundBackRight(SpeakerBase):
    _key = 'surroundBackR'


class FrontHighLeft(SpeakerBase):
    _key = 'frontHighL'


class FrontHightRight(SpeakerBase):
    _key = 'frontHighR'


class FrontHigh(PositionBase):
    _key = 'frontHigh'

    def __init__(self, sony_api):
        PositionBase.__init__(self, sony_api)
        self.left = FrontHighLeft(sony_api)
        self.right = FrontHightRight(sony_api)


class Front(PositionBase):
    _key = 'front'

    def __init__(self, sony_api):
        PositionBase.__init__(self, sony_api)
        self.left = FrontLeft(sony_api)
        self.right = FrontRight(sony_api)
        self.high = FrontHigh(sony_api)
        self.center = Center(sony_api)

    @property
    def speaker_position(self):
        """
        Gets the type of front and center speaker.

        Floor speaker or In-Ceiling speaker

        :return: Returned values will be one of the following:
            "floor" - Speaker position is Floor speaker.
            "inCeiling" - Speaker position is In-Ceiling speaker.
        :rtype: str
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self._key = ''
        try:
            return self.__send('speakerPosition')
        finally:
            self._key = 'front'

    @speaker_position.setter
    def speaker_position(self, value):
        """
        Sets the type of front and center speaker.
        Floor speaker or In-Ceiling speaker

        :param value: One of the following:
            "floor" - Speaker position is Floor speaker.
            "inCeiling" - Speaker position is In-Ceiling speaker.
        :type value: str
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self._key = ''
        self.__send('speakerPosition', value=value)
        self._key = 'front'

    @property
    def ceiling_height(self):
        """
        Gets the height from the floor to the ceiling speakers.

        (Unit: mm)

        :return: Returned values will be between 2000 (min) and 10000 (max)
            with a step of 10.
        :rtype: int
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self._key = ''
        try:
            return self.__send('ceilingSpeakerHeight')
        finally:
            self._key = 'front'

    @ceiling_height.setter
    def ceiling_height(self, value):
        """
        Sets the height from the floor to the ceiling speakers.

        (Unit: mm)

        :param value: values will be between 2000 (min) and 10000 (max)
            with a step of 10.
        :type value: int
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self._key = ''
        self.__send('ceilingSpeakerHeight', value=value)
        self._key = 'front'

    @property
    def in_ceiling_speaker_mode(self):
        """
        Gets in-ceiling speaker mode for the current input.

        In a setup where the front and center speakers are installed in the
        ceiling, lowering the audio output position to the screen height allows
        you to enjoy a more natural experience.

        :return: Returned values will be one of the following:
            True - "on", Enable In Ceiling Speaker Mode.
            False - "off", Disable In Ceiling Speaker Mode.
        :rtype: bool
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self._key = ''
        try:
            return (
                True if self.__send('inCeilingSpeakerMode') == 'on' else False
            )
        finally:
                self._key = 'front'

    @in_ceiling_speaker_mode.setter
    def in_ceiling_speaker_mode(self, value):
        """
        Sets whether or not to use in-ceiling speaker mode with the current
        input.

        In a setup where the front and center speakers are installed in the
        ceiling, lowering the audio output position to the screen height allows
        you to enjoy a more natural experience.

        :param value: True - "on", False - "off"
        :type value: bool
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self._key = ''
        self.__send('inCeilingSpeakerMode', value='on' if value else 'off')
        self._key = 'front'


class SurroundBack(SpeakerBase):
    _key = 'surroundBack'

    def __init__(self, sony_api):
        SpeakerBase.__init__(self, sony_api)
        self.left = SurroundBackLeft(sony_api)
        self.right = SurroundBackRight(sony_api)

    @property
    def zone_assignment(self):
        """
        Gets Surround Back speaker output assignment.

        :return: Returned values will be one of the following:
            "zone2" - Surround back speaker is assigned for Zone 2. When using
            the Zone 2 connection.
            "biAmp" - Surround back speaker is assigned for Bi-Amp. When using
            the bi-amplifier connection.
            "frontB" - Surround back speaker is assigned for Front B. When
            using the front B speaker connection.
            "off" - When none of the connections above are used.
        :rtype: str
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """

        return self.__send('SpeakerAssign')

    @zone_assignment.setter
    def zone_assignment(self, value):
        """
        Sets Surround Back speaker output assignment.

        :param value: One of the following:
            "zone2" - Surround back speaker is assigned for Zone 2. When using
            the Zone 2 connection.
            "biAmp" - Surround back speaker is assigned for Bi-Amp. When using
            the bi-amplifier connection.
            "frontB" - Surround back speaker is assigned for Front B. When
            using the front B speaker connection.
            "off" - When none of the connections above are used.
        :type value: str
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self.__send('SpeakerAssign', value=value)


class Surround(PositionBase, SpeakerBase):
    _key = 'surround'

    def __init__(self, sony_api):
        PositionBase.__init__(self, sony_api)
        SpeakerBase.__init__(self, sony_api)
        self.left = SurroundLeft(sony_api)
        self.right = SurroundRight(sony_api)
        self.back = SurroundBack(sony_api)

    @property
    def zone_assignment(self):
        """
        Gets Surround speaker output assignment.

        :return: Returned values will be one of the following:
            "zone3" - Surround speaker is assigned for Zone 3.
            "off" - Surround speaker is not assigned for Zone 3.
        :rtype: str
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        return self.__send('SpeakerAssign')

    @zone_assignment.setter
    def zone_assignment(self, value):
        """
        Sets Surround speaker output assignment.

        :param value: One of the following:
            "zone3" - Surround speaker is assigned for Zone 3.
            "off" - Surround speaker is not assigned for Zone 3.
        :type value: str
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self.__send('SpeakerAssign', value=value)


class Subwoofer(PositionBase, SpeakerBase):
    _key = 'subwoofer'

    def __init__(self, sony_api):
        PositionBase.__init__(self, sony_api)
        SpeakerBase.__init__(self, sony_api)

    @property
    def level(self):
        """
        Gets level of Subwoofer.

        Note that the range and step values vary depending on device.

        :return: Returned values will be between -0 (min) and 24 (max)
            with a step of 1
        :rtype: int
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """

        return self.__send('Level')

    @level.setter
    def level(self, value):
        """
        Sets level of Subwoofer.

        Note that the range and step values vary depending on device.

        :param value: values will be between 0 (min) and 24 (max)
            with a step of 1.
        :type value: int
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self.__send('Level', value=value)

    @property
    def crossover_frequency(self):
        """
        Gets the cut off frequency of the Wireless Subwoofer.

        All frequencies below the cut off frequency are output to the Wireless
        Subwoofer instead of the TV speakers.

        :return: Returned values will be between 0 (min) and 30 (max)
            with a step of 1
        :rtype: int
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        return self.__send('Freq')

    @crossover_frequency.setter
    def crossover_frequency(self, value):
        """
        Sets the cut off frequency of the Wireless Subwoofer.

        All frequencies below the cut off frequency are output to the Wireless
        Subwoofer instead of the TV speakers.

        :param value: values will be between 0 (min) and 30 (max)
            with a step of 1.
        :type value: int
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self.__send('Freq', value=value)

    @property
    def phase(self):
        """
        Gets the phase polarity of subwoofer.

        :return: Returned values will be one of the following:
            "normal" - normal
            "reverse" - reverse
        :rtype: str
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        return self.__send('Phase')

    @phase.setter
    def phase(self, value):
        """
        Sets the phase polarity of subwoofer.

        :param value: One of the following:
            "normal" - normal
            "reverse" - reverse
        :type value: str
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self.__send('Phase', value=value)

    @property
    def power(self):
        """
        Gets the power control method of the Wireless Subwoofer.

        :return: Returned values will be one of the following:
            True - "on"
            False - "off"
        :rtype: bool
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        return self.__send('Power') == "on"

    @power.setter
    def power(self, value):
        """
        Sets the power control method of the Wireless Subwoofer.

        :param value: True - "on", False - "off"
        :type value: bool
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self.__send('Power', value='on' if value else 'off')

    @property
    def low_pass_filter(self):
        """
        Gets the low-pass filter state for the subwoofer.

        The low-pass filter works when PCM signals are input via an all
        connection. Turn the function on if connecting a subwoofer without
        the crossover frequency function.

        :return: Returned values will be one of the following:
            True - "on" The low-pass filter of subwoofer is enabled.
            False - "off" - The low-pass filter of subwoofer is disabled.
        :rtype: bool
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        return self.__send('Lpf') == 'on'

    @low_pass_filter.setter
    def low_pass_filter(self, value):
        """
        Sets the low-pass filter state for the subwoofer.

        The low-pass filter works when PCM signals are input via an all
        connection. Turn the function on if connecting a subwoofer without
        the crossover frequency function.

        :param value: True - "on", False - "off"
        :type value: bool
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self.__send('Lpf', value='on' if value else 'off')

    @property
    def hdmi_pcm_level(self):
        """
        Gets the PCM level of the subwoofer.

        The level for each input to which an HDMI
        input jack is assigned can be set independently.
        0 dB or +10 dB when PCM signals are  input via an HDMI connection.

        :return: Returned values will be one of the following:
            "auto" - Automatically sets the level to 0 dB or +10 dB, depending
            on the audio stream.
            "10db" - Subwoofer Speaker Level is set to +10 dB.
            "0db" - Subwoofer Speaker Level is set to 0 dB.
        :rtype: str
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """

        return self.__send('LevelHdmiPcm')

    @hdmi_pcm_level.setter
    def hdmi_pcm_level(self, value):
        """
        Sets the PCM level of the subwoofer.

        The level for each input to which an HDMI
        input jack is assigned can be set independently.
        0 dB or +10 dB when PCM signals are  input via an HDMI connection.

        :param value: One of the following:
            "auto" - Automatically sets the level to 0 dB or +10 dB, depending
            on the audio stream.
            "10db" - Subwoofer Speaker Level is set to +10 dB.
            "0db" - Subwoofer Speaker Level is set to 0 dB.
        :type value: str
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """

        self.__send('LevelHdmiPcm', value=value)


class Center(PositionBase, SpeakerBase):
    _key = 'center'

    def __init__(self, sony_api):
        PositionBase.__init__(self, sony_api)
        SpeakerBase.__init__(self, sony_api)

    @property
    def up_lift(self):
        """
        Gets the Center channel uplift level.

        :return: Returned values will be between 0 (min) and 10 (max)
            with a step of 1.
            0 being "off" - Disable lifting up the sound of the center speaker.
        :rtype: int
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        value = self.__send('LiftUp')

        if value == 'off':
            value = 0

        return value

    @up_lift.setter
    def up_lift(self, value):
        """
        Sets the Center channel uplift level.

        :param value: values will be between 0 (min) and 10 (max)
            with a step of 1.
            0 being "off" - Disable lifting up the sound of the center speaker.
        :type value: int
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self.__send('LiftUp', value=value if value else 'off')


class Settings(object):
    """
    Speaker Settings

    API Layout
    items that do not have a "." at the end of them are properties.

    Settings.
        tv_position
        speaker_selection
        distance_unit
        speaker_pattern
        front.
            speaker_position
            ceiling_height
            in_ceiling_speaker_mode
            size
            crossover_frequency
            left.
                level
                distance
            right.
                level
                distance
            center.
                level
                distance
                size
                crossover_frequency
                up_lift
            high.
                size
                crossover_frequency
                left.
                    level
                    distance
                right.
                    level
                    distance

        surround.
            zone_assignment
            level
            distance
            size
            crossover_frequency
            left.
                level
                distance
            right.
                level
                distance
            back.
                level
                distance
                zone_assignment
                size
                crossover_frequency
                left.
                    level
                    distance
                right.
                    level
                    distance
        subwoofer.
            level
            crossover_frequency
            phase
            power
            low_pass_filter
            hdmi_pcm_level
    """

    _key = ''

    def __init__(self, sony_api):
        self.__sony_api = sony_api

        self.front = Front(sony_api)
        self.surround = Surround(sony_api)
        self.subwoofer = Subwoofer(sony_api)

    def __send(self, *args, **kwargs):
        return self.__sony_api.send(self, *args, **kwargs)

    @property
    def tv_position(self):
        """
        Gets the TV position sound setting.

        :return: Returned values will be one of the following:
            "tableTop" - Provides the best sound quality when you place the TV
            on a TV stand.
            "wallMount" - Provides the best sound quality when you hang the TV
            on a wall.
        :rtype: str
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        return self.__send('tvPosition')

    @tv_position.setter
    def tv_position(self, value):
        """
        Sets the TV position sound setting.

        :param value: One of the following:
            "tableTop" - Provides the best sound quality when you place the TV
            on a TV stand.
            "wallMount" - Provides the best sound quality when you hang the TV
            on a wall.
        :type value: str
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self.__send('tvPosition', value=value)

    @property
    def speaker_selection(self):
        """
        Gets the Front speaker output selection.

        :return: Returned values will be one of the following:
            "speakerA" - Speaker A. Speakers connected to the SPEAKERS FRONT A
            terminals.
            "speakerB" - Speaker B. Speakers connected to the SPEAKERS SURROUND
            BACK/BI-AMP/FRONT HIGH/FRONT B terminals.
            "speakerA_B" - Speaker A and Speaker B. Speakers connected to both
            the SPEAKERS FRONT A and SPEAKERS SURROUND BACK/BIAMP/FRONT
            HIGH/FRONT B terminals (parallel connection).
            "off" - No audio signals are output from any speaker terminals.
        :rtype: str
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        return self.__send('speakerSelection')

    @speaker_selection.setter
    def speaker_selection(self, value):
        """
        Sets the Front speaker output selection.

        :param value: One of the following:
            "speakerA" - Speaker A. Speakers connected to the SPEAKERS FRONT A
            terminals.
            "speakerB" - Speaker B. Speakers connected to the SPEAKERS SURROUND
            BACK/BI-AMP/FRONT HIGH/FRONT B terminals.
            "speakerA_B" - Speaker A and Speaker B. Speakers connected to both
            the SPEAKERS FRONT A and SPEAKERS SURROUND BACK/BIAMP/FRONT
            HIGH/FRONT B terminals (parallel connection).
            "off" - No audio signals are output from any speaker terminals.
        :type value: str
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self.__send('speakerSelection', value=value)

    @property
    def distance_unit(self):
        """
        Gets the unit of measure. (Distance Unit)

        :return: Returned values will be one of the following:
            "meter" - The distance is displayed in meters.
            "feet" - The distance is displayed in feet.
        :rtype: str
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        return self.__send('distanceUnit')

    @distance_unit.setter
    def distance_unit(self, value):
        """
        Sets the unit of measure. (Distance Unit)

        :param value: One of the following:
            "meter" - The distance is displayed in meters.
            "feet" - The distance is displayed in feet.
        :type value: str
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self.__send('distanceUnit', value=value)

    @property
    def speaker_pattern(self):
        """
        Gets the speaker pattern.

        :return: Returned values will be one of the following:
            "2_0_0" - Speaker pattern is 2/0
            "2_0_1" - Speaker pattern is 2/0.1
            "3_0_0" - Speaker pattern is 3/0
            "3_0_1" - Speaker pattern is 3/0.1
            "2_2_0" - Speaker pattern is 2/2
            "2_2_1" - Speaker pattern is 2/2.1
            "3_2_0" - Speaker pattern is 3/2
            "3_2_1" - Speaker pattern is 3/2.1
            "2_3_0" - Speaker pattern is 2/3
            "2_3_1" - Speaker pattern is 2/3.1
            "3_3_0" - Speaker pattern is 3/3
            "3_3_1" - Speaker pattern is 3/3.1
            "2_4_0" - Speaker pattern is 2/4
            "2_4_1" - Speaker pattern is 2/4.1
            "3_4_0" - Speaker pattern is 3/4
            "3_4_1" - Speaker pattern is 3/4.1
            "4_2_0" - Speaker pattern is 4/2
            "4_2_1" - Speaker pattern is 4/2.1
            "5_2_0" - Speaker pattern is 5/2
            "5_2_1" - Speaker pattern is 5/2.1
        :rtype: str
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        return self.__send('speakerPattern')

    @speaker_pattern.setter
    def speaker_pattern(self, value):
        """
        Sets the speaker pattern.

        :param value: One of the following:
            "2_0_0" - Speaker pattern is 2/0
            "2_0_1" - Speaker pattern is 2/0.1
            "3_0_0" - Speaker pattern is 3/0
            "3_0_1" - Speaker pattern is 3/0.1
            "2_2_0" - Speaker pattern is 2/2
            "2_2_1" - Speaker pattern is 2/2.1
            "3_2_0" - Speaker pattern is 3/2
            "3_2_1" - Speaker pattern is 3/2.1
            "2_3_0" - Speaker pattern is 2/3
            "2_3_1" - Speaker pattern is 2/3.1
            "3_3_0" - Speaker pattern is 3/3
            "3_3_1" - Speaker pattern is 3/3.1
            "2_4_0" - Speaker pattern is 2/4
            "2_4_1" - Speaker pattern is 2/4.1
            "3_4_0" - Speaker pattern is 3/4
            "3_4_1" - Speaker pattern is 3/4.1
            "4_2_0" - Speaker pattern is 4/2
            "4_2_1" - Speaker pattern is 4/2.1
            "5_2_0" - Speaker pattern is 5/2
            "5_2_1" - Speaker pattern is 5/2.1
        :type value: str
        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError, if feature not available.
        """
        self.__send('speakerPattern', value=value)
