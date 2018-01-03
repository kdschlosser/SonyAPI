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
from ..exception import UnsupportedError


class Settings(object):

    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, target, **params):
        setting = self.__sony_api.send(
            'audio',
            'getSoundSettings',
            target=target
        )[0][0]

        if params:
            for value in setting['candidate']:
                if value['value'] == params['value']:
                    if value['isAvailable']:
                        params['target'] = target
                        self.__sony_api.send(
                            'audio',
                            'setSoundSettings',
                            settings=[params]
                        )
                    else:
                        raise UnsupportedError
                    break
            else:
                raise UnsupportedError
        else:
            return setting['currentValue']

    @property
    def digital_audio_type(self):

        """
        Gets the output type for the digital signal from HDMI or DIGITAL OUT

        :return: Possible values:
            "auto" - PCM and BitStream can switch automatically according to
                connection device.
            "pcm" - PCM output from HDMI or digital audio output.
            "multiPcm" - Multi channel PCM output from HDMI or digital audio
                output.
            "2chPcm" - 2 channel PCM output from HDMI or digital audio output.
        :rtype: str
        """
        return self.__send('digitalAudioType')

    @digital_audio_type.setter
    def digital_audio_type(self, value):
        """
        Sets the output type for the digital signal from HDMI or DIGITAL OUT

        :param value: Possible values:
            "auto" - PCM and BitStream can switch automatically according to
                connection device.
            "pcm" - PCM output from HDMI or digital audio output.
            "multiPcm" - Multi channel PCM output from HDMI or digital audio
                output.
            "2chPcm" - 2 channel PCM output from HDMI or digital audio output.
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('digitalAudioType', value=value)

    @property
    def dsd_mode(self):
        """
        Gets Audio output mode from HDMI during SACD or DSD file format
        playback.

        :return: Possible values:
            "auto" - DSD output
            "off" - PCM output
        :rtype: str
        """
        return self.__send('dsdMode')

    @dsd_mode.setter
    def dsd_mode(self, value):
        """
        Sets Audio output mode from HDMI during SACD or DSD file format
        playback.

        :param value: Possible values:
            "auto" - DSD output
            "off" - PCM output
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('dsdMode', value=value)

    @property
    def bd_mix_mode(self):
        """
        Gets Mix state of Audio output during BDMV playback.

        :return: Possible values:
            True - "on", Outputs Mixed Audio, that is Additional Audio mixed
                with Primary Audio.
            False - "off", Outputs only Primary Audio.
        :rtype: bool
        """
        return self.__send('bdMixMode') == 'on'

    @bd_mix_mode.setter
    def bd_mix_mode(self, value):
        """
        Sets Mix state of Audio output during BDMV playback.

        :param value: Possible values:
            True - "on", Outputs Mixed Audio, that is Additional Audio mixed
                with Primary Audio.
            False - "off", Outputs only Primary Audio.
        :type value: bool
        :return: None
        :rtype: None
        """
        self.__send('bdMixMode', value='on' if value else 'off')

    @property
    def aac(self):
        """
        Gets the output method of AAC signal.

        :return: Possible values:
            "downmixPcm" - Converted Downmix LPCM output
            "aac" - AAC output
        :rtype: str
        """
        return self.__send('aac')

    @aac.setter
    def aac(self, value):
        """
        Sets the output method of AAC signal.

        :param value: Possible values:
            "downmixPcm" - Converted Downmix LPCM output
            "aac" - AAC output
        :type value: str

        :return: None
        :rtype: None
        """
        self.__send('aac', value=value)

    @property
    def digital_music_enhancer(self):
        """
        Gets Digital Music Enhancer settings.

        Output when playing Internet content or USB content.

        :return: Possible values:
            "on" - Three elements (PAE+(Portable Audio Enhancer Plus), Dynamic
                Range Recovery, Advanced Auto Volume) are enabled to create
                better sound quality for Internet content or USB content.
            "off" - Turns off the Digital Music Enhancer function.
            "soundBarMode" - Same as setting value "off", the purpose of this
                setting value is to force sound bar users to use off.
        :rtype: str
        """
        return self.__send('digitalMusicEnhancer')

    @digital_music_enhancer.setter
    def digital_music_enhancer(self, value):
        """
        Sets Digital Music Enhancer settings.

        Output when playing Internet content or USB content.

        :param value: Possible values:
            "on" - Three elements (PAE+(Portable Audio Enhancer Plus), Dynamic
                Range Recovery, Advanced Auto Volume) are enabled to create
                better sound quality for Internet content or USB content.
            "off" - Turns off the Digital Music Enhancer function.
            "soundBarMode" - Same as setting value "off", the purpose of this
                setting value is to force sound bar users to use off.
        :type value: str

        :return: None
        :rtype: None
        """
        self.__send('digitalMusicEnhancer', value=value)

    @property
    def dts_neo_6(self):
        """
        Gets settings for DTS Neo:6.

        :return: Possible values:
            "cinema" - Neo:6 Cinema settings for movie.
            "music" - Neo:6 Music settings for audio.
            "off" - Disable Neo:6 function.
        :rtype: str
        """
        return self.__send('dtsNeo6')

    @dts_neo_6.setter
    def dts_neo_6(self, value):
        """
        Sets settings for DTS Neo:6.

        :param value: Possible values:
            "cinema" - Neo:6 Cinema settings for movie.
            "music" - Neo:6 Music settings for audio.
            "off" - Disable Neo:6 function.
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('dtsNeo6', value=value)

    @property
    def convert_to_dolby_d(self):
        """
        Gets Dolby Digital Converter Dolby D Compatible Output.

        Converts DTS source to Dolby Digital by referring EDID.

        :return: Possible values:
            True - "on", Convert DTS source to Dolby Digital by referring EDID.
            False - "off", Not convert DTS source to Dolby Digital
        :rtype: bool

        """
        return self.__send('convertToDolbyD') == 'on'

    @convert_to_dolby_d.setter
    def convert_to_dolby_d(self, value):
        """
        Sets Dolby Digital Converter Dolby D Compatible Output.

        Converts DTS source to Dolby Digital by referring EDID.

        :param value: Possible values:
            True - "on", Convert DTS source to Dolby Digital by referring EDID.
            False - "off", Not convert DTS source to Dolby Digital
        :return: None
        :type value: None
        """
        self.__send('convertToDolbyD', value='on' if value else 'off')

    @property
    def input_attenuation(self):
        """
        Gets input sensitivity of audio signal input to Audio analog audio
        input terminal.

        :return: Possible values:
            True - "on", Enable input attenuation function
            False - "off", Disable input attenuation function
        :rtype: bool
        """
        return self.__send('inputAttenuation') == 'on'

    @input_attenuation.setter
    def input_attenuation(self, value):
        """
        Sets input sensitivity of audio signal input to Audio analog audio
        input terminal.

        :param value: Possible values:
            True - "on", Enable input attenuation function
            False - "off", Disable input attenuation function
        :type value: bool
        :return: None
        :rtype: None
        """
        self.__send('inputAttenuation', value='on' if value else 'off')

    @property
    def output_terminal(self):
        """
        Gets speakers or terminals to output sound.

        :return: Possible values:
            "speaker" - Audio is output from speaker.
            "speaker_hdmi" - Audio is output from speaker and HDMI.
            "hdmi" - Audio is output from HDMI.
            "audioSystem" - Audio is output from HDMI or digital audio output.
            "line" - Audio is output from line output.
        :rtype: str
        """
        return self.__send('outputTerminal')

    @output_terminal.setter
    def output_terminal(self, value):
        """
        Sets speakers or terminals to output sound.

        :param value: Possible values:
            "speaker" - Audio is output from speaker.
            "speaker_hdmi" - Audio is output from speaker and HDMI.
            "hdmi" - Audio is output from HDMI.
            "audioSystem" - Audio is output from HDMI or digital audio output.
            "line" - Audio is output from line output.
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('outputTerminal', value=value)

    @property
    def audio_drc(self):
        """
        Gets Dynamic Range Control (DRC)

        Makes even small sounds more audible when listening in low volume.

        :return: Possible values:
            "auto" - Dynamic range specified by disc is set. (only BD-ROM)
            "on" - Dynamic range specified by recording engineer is set.
            "off" - Disable DRC function.
            "standard" - Dynamic range is adjusted between "tv" and
                "wideRange".
            "tv" - a faint sound is emphasized for TV speaker
            "wideRange" - you can enjoy dynamic sound. This is more effective
                when using Hi-Fi speaker.
        :rtype: str
        """
        return self.__send('audioDRC')

    @audio_drc.setter
    def audio_drc(self, value):
        """
        Sets Dynamic Range Control (DRC)

        Makes even small sounds more audible when listening in low volume.

        :param value: Possible values:
            "auto" - Dynamic range specified by disc is set. (only BD-ROM)
            "on" - Dynamic range specified by recording engineer is set.
            "off" - Disable DRC function.
            "standard" - Dynamic range is adjusted between "tv" and
                "wideRange".
            "tv" - a faint sound is emphasized for TV speaker
            "wideRange" - you can enjoy dynamic sound. This is more effective
                when using Hi-Fi speaker.
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('audioDRC', value=value)

    @property
    def down_mix(self):
        """
        Gets Down Mix mode.

        Enabled when outputting BD LPCM, DTS HD, Dolby TrueHD, DD+, DD, DTS
        and AAC of Multi Channel source by Downmixed PCM 2ch. Multi channel
        source BD LPCM, DTS HD, Dolby TrueHD, DD+, DD, DTS, AAC are able to
        export when set as Downmix in PCM 2ch.

        :return: Possible values:
            "surround" - Audio with surround effect is output.
            "stereo" - Audio without surround effect is output.
        :rtype: str
        """
        return self.__send('downMix')

    @down_mix.setter
    def down_mix(self, value):
        """
        Sets Down Mix mode.

        Enabled when outputting BD LPCM, DTS HD, Dolby TrueHD, DD+, DD, DTS
        and AAC of Multi Channel source by Downmixed PCM 2ch. Multi channel
        source BD LPCM, DTS HD, Dolby TrueHD, DD+, DD, DTS, AAC are able to
        export when set as Downmix in PCM 2ch.

        :param value: Possible values:
            "surround" - Audio with surround effect is output.
            "stereo" - Audio without surround effect is output.
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('downMix', value=value)

    @property
    def auto_genre_selector(self):
        """
        Gets Genre Selector

        To provide suitable Sound Field depending on the kind of contents,
        switch Sound Field automatically according to "Genre Info" on CEC.

        :return: Possible values:
            True - "on", Enable Auto Genre Selector function.
            False - "off", The Auto Genre selector function is disable.
        :rtype: bool
        """
        return self.__send('autoGenreSelector')

    @auto_genre_selector.setter
    def auto_genre_selector(self, value):
        """
        Sets Genre Selector

        To provide suitable Sound Field depending on the kind of contents,
        switch Sound Field automatically according to "Genre Info" on CEC.

        :param value: Possible values:
            True - "on", Enable Auto Genre Selector function.
            False - "off", The Auto Genre selector function is disable.
        :type value: bool
        :return: None
        :rtype: None
        """
        self.__send('autoGenreSelector', value='on' if value else 'off')

    @property
    def dsee_hx(self):
        """
        Gets whether using the DSEE HX function.

        DSEE HX is advanced DSEE (Digital Sound Enhancement Engine) function
        and up scales existing sound sources to near hi-resolution sound
        quality.

        :return: Possible values:
            "auto" - Enable DSEE HX function only when sound is 2ch.
            "on" - Enable DSEE HX function always regardless of the number of
                channel.
            "off" - Disable DSEE HX function.
        :rtype: str
        """
        return self.__send('dseeHX')

    @dsee_hx.setter
    def dsee_hx(self, value):
        """
        Sets whether using the DSEE HX function.

        DSEE HX is advanced DSEE (Digital Sound Enhancement Engine) function
        and up scales existing sound sources to near hi-resolution sound
        quality.

        :param value: Possible values:
            "auto" - Enable DSEE HX function only when sound is 2ch.
            "on" - Enable DSEE HX function always regardless of the number of
                channel.
            "off" - Disable DSEE HX function.
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('dseeHXTmp', value=value)

    @property
    def dsee_hx_tmp(self):
        """
        Gets whether using the DSEE HX Tmp function.

        DSEE HX is advanced DSEE (Digital Sound Enhancement Engine) function
        and up scales existing sound sources to near hi-resolution sound
        quality.

        :return: Possible values:
            "auto" - Enable DSEE HX function only when sound is 2ch.
            "on" - Enable DSEE HX function always regardless of the number of
                channel.
            "off" - Disable DSEE HX function.
        :rtype: str
        """
        return self.__send('dseeHX')

    @dsee_hx_tmp.setter
    def dsee_hx_tmp(self, value):
        """
        Sets whether using the DSEE HX Tmp function.

        DSEE HX is advanced DSEE (Digital Sound Enhancement Engine) function
        and up scales existing sound sources to near hi-resolution sound
        quality.

        :param value: Possible values:
            "auto" - Enable DSEE HX function only when sound is 2ch.
            "on" - Enable DSEE HX function always regardless of the number of
                channel.
            "off" - Disable DSEE HX function.
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('dseeHXTmp', value=value)

    @property
    def clear_audio(self):
        """
        Gets Clear Audio+ function

        :return: Possible values:
            True - "on", Enable Clear Audio + function
            False - "off", Disable Clear Audio + function
        :rtype: bool
        """
        return self.__send('clearAudio')

    @clear_audio.setter
    def clear_audio(self, value):
        """
        Gets Clear Audio+ function

        :param value: Possible values:
            True - "on", Enable Clear Audio + function
            False - "off", Disable Clear Audio + function
        :type value: bool
        :return: None
        :rtype: None
        """
        self.__send('clearAudio', value='on' if value else 'off')

    @property
    def football_mode(self):
        """
        Gets Football Mode

        :return: Possible values:
            "on" - Enable Football Mode with narration
            "on_narration_off" - Enable Football Mode without narration
            "off" - Disable Football Mode
        :rtype: str
        """
        return self.__send('footballMode')

    @football_mode.setter
    def football_mode(self, value):
        """
        Sets Football Mode

        :param value: Possible values:
            "on" - Enable Football Mode with narration
            "on_narration_off" - Enable Football Mode without narration
            "off" - Disable Football Mode
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('footballMode', value=value)

    @property
    def auto_format_direct_2ch(self):
        """
        Gets Auto Format Direct (A.F.D)/2-channel sound mode

        :return: Possible values:
            "2chStereo" - 2ch Stereo.
                The receiver outputs the sound from the front left/right
                speakers only. There is no sound from the subwoofer.
            "analogDirect" - Analog Direct.
                You can switch the audio of the selected input to 2-channel
                analog input. This function enables you to enjoy high-quality
                analog sources.
            "auto" - Auto Format Direct (A.F.D.).
                Presets the sound as it was recorded/encoded without adding any
                surround effects.
            "multiStereo" - Multi stereo.
                Outputs 2-channel left/right or monaural signals from all
                speakers.
            "off" - Disable A.F.D/2ch function
        :rtype: str
        """
        return self.__send('autoFormatDirect_2ch')

    @auto_format_direct_2ch.setter
    def auto_format_direct_2ch(self, value):
        """
        Sets Auto Format Direct (A.F.D)/2-channel sound mode

        :param value: Possible values:
            "2chStereo" - 2ch Stereo.
                The receiver outputs the sound from the front left/right
                speakers only. There is no sound from the subwoofer.
            "analogDirect" - Analog Direct.
                You can switch the audio of the selected input to 2-channel
                analog input. This function enables you to enjoy high-quality
                analog sources.
            "auto" - Auto Format Direct (A.F.D.).
                Presets the sound as it was recorded/encoded without adding any
                surround effects.
            "multiStereo" - Multi stereo.
                Outputs 2-channel left/right or monaural signals from all
                speakers.
            "off" - Disable A.F.D/2ch function
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('autoFormatDirect_2ch', value=value)

    @property
    def sound_field(self):
        """
        Gets the sound quality according to the music genre.

        :return: Possible values:
            "standard" - Music Equalizer Standard.
                Sound effects are optimized for the individual source.
            "rock" - Music Equalizer Rock
            "hiphop" - Music Equalizer Hip Hop
            "electronica" - Music Equalizer Electronica
            "sertanejo" - Music Equalizer Sertanejo
            "movie" - Movie mode.
                Sound effects are optimized for movies. This mode replicates
                the density and rich expanse of sound.
            "movie2" - Movie2 mode.
                Sound effects are optimized for movies. This mode replicates
                sound looping around the listener to the rear.
            "music" - Music mode.
                Sound effects are optimized for music.
            "game" - Game mode.
                Sound effects are optimized for game play.
            "compressionMusic" - Digital Music mode
            "night" - Night mode
            "flat" - Flat mode
            "pop" - Pop mode
            "jazz" - Jazz mode.
                Reproduces the acoustics of a jazz club.
            "latin" - Latin mode
            "classic" - Classic mode
            "custom" - Custom mode
            "clearAudio" - Clear Audio + mode.
                The appropriate sound setting is automatically selected for the
                sound source.
            "sports" - Sports mode.
                Reproduces the feel of sports broadcasting.
            "live" - Live mode.
                Reproduces the acoustics of a 300-seat live house.
            "stadium" - Stadium mode.
                Reproduces the feel of a large open-air stadium
            "proLogicIIMusic" - Pro Logic II Music mode.
                Performs Dolby Pro Logic II Music mode decoding. This setting
                is ideal for normal stereo sources such as CDs.
            "proLogicIIxMusic" - Pro Logic IIx Music mode.
                Performs Dolby Pro Logic IIx Music mode decoding. This setting
                is ideal for normal stereo sources such as CDs.
            "neo6Music" - Neo6 Music mode.
                Performs DTS Neo:6 Music mode decoding. Sources recorded in
                2-channel format are enhanced up to 7 channels. This setting is
                ideal for normal stereo sources such as CDs.
            "concertHallA" - Concert Hall A.
                Reproduces the acoustics of a vineyard style concert hall in
                Berlin famous for its clear acoustics.
            "concertHallB" - Concert Hall B.
                Reproduces the acoustics of a shoe box style concert hall with
                plaster walls in Amsterdam.
            "concertHallC" - Concert Hall C.
                Reproduces the acoustics of a wooden shoe box style concert
                hall in Vienna.
            "portableAudio" - Portable Audio.
                Reproduces clear enhanced sound from your portable audio
                device. This mode is ideal for MP3s and other compressed music.
            "cinemaStudio" - Cinema Studio.
                Sound effect are optimized for higher realistic sound like a
                cinema studio.
            "musicArena" - Music Arena.
                Sound effects like a live music concerts filled with great
                excitement created by Sony’s unique Audio DSP technology.
            "headPhone2ch" - This mode is selected automatically when
                connecting headphones. Standard 2-channel stereo sources
                completely bypass the sound field processing and multi-channel
                surround formats are downmixed to 2 channels except LFE
                signals.
            "off" - Disable Sound Field function.
        :rtype: str
        """
        return self.__send('soundField')

    @sound_field.setter
    def sound_field(self, value):
        """
        Sets the sound quality according to the music genre.

        :param value: Possible values:
            "standard" - Music Equalizer Standard.
                Sound effects are optimized for the individual source.
            "rock" - Music Equalizer Rock
            "hiphop" - Music Equalizer Hip Hop
            "electronica" - Music Equalizer Electronica
            "sertanejo" - Music Equalizer Sertanejo
            "movie" - Movie mode.
                Sound effects are optimized for movies. This mode replicates
                the density and rich expanse of sound.
            "movie2" - Movie2 mode.
                Sound effects are optimized for movies. This mode replicates
                sound looping around the listener to the rear.
            "music" - Music mode.
                Sound effects are optimized for music.
            "game" - Game mode.
                Sound effects are optimized for game play.
            "compressionMusic" - Digital Music mode
            "night" - Night mode
            "flat" - Flat mode
            "pop" - Pop mode
            "jazz" - Jazz mode.
                Reproduces the acoustics of a jazz club.
            "latin" - Latin mode
            "classic" - Classic mode
            "custom" - Custom mode
            "clearAudio" - Clear Audio + mode.
                The appropriate sound setting is automatically selected for the
                sound source.
            "sports" - Sports mode.
                Reproduces the feel of sports broadcasting.
            "live" - Live mode.
                Reproduces the acoustics of a 300-seat live house.
            "stadium" - Stadium mode.
                Reproduces the feel of a large open-air stadium
            "proLogicIIMusic" - Pro Logic II Music mode.
                Performs Dolby Pro Logic II Music mode decoding. This setting
                is ideal for normal stereo sources such as CDs.
            "proLogicIIxMusic" - Pro Logic IIx Music mode.
                Performs Dolby Pro Logic IIx Music mode decoding. This setting
                is ideal for normal stereo sources such as CDs.
            "neo6Music" - Neo6 Music mode.
                Performs DTS Neo:6 Music mode decoding. Sources recorded in
                2-channel format are enhanced up to 7 channels. This setting is
                ideal for normal stereo sources such as CDs.
            "concertHallA" - Concert Hall A.
                Reproduces the acoustics of a vineyard style concert hall in
                Berlin famous for its clear acoustics.
            "concertHallB" - Concert Hall B.
                Reproduces the acoustics of a shoe box style concert hall with
                plaster walls in Amsterdam.
            "concertHallC" - Concert Hall C.
                Reproduces the acoustics of a wooden shoe box style concert
                hall in Vienna.
            "portableAudio" - Portable Audio.
                Reproduces clear enhanced sound from your portable audio
                device. This mode is ideal for MP3s and other compressed music.
            "cinemaStudio" - Cinema Studio.
                Sound effect are optimized for higher realistic sound like a
                cinema studio.
            "musicArena" - Music Arena.
                Sound effects like a live music concerts filled with great
                excitement created by Sony’s unique Audio DSP technology.
            "headPhone2ch" - This mode is selected automatically when
                connecting headphones. Standard 2-channel stereo sources
                completely bypass the sound field processing and multi-channel
                surround formats are downmixed to 2 channels except LFE
                signals.
            "off" - Disable Sound Field function.
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('soundField', value=value)

    @property
    def sound_field_movie(self):
        """
        Gets Sound Field Movie function.

        :return: Possible values:
            "hdDcsDynamic" - HD Digital Cinema Sound (HD-D.C.S.) Dynamic.
                This setting is suitable for an environment which is
                reverberant but lacks a spacious feel (where sound absorption
                is not sufficient). It emphasizes the reflection of sound and
                reproduces the sound of a large, classic movie theater.
            "hdDcsTheater" - HD Digital Cinema Sound (HD-D.C.S.) Theater.
                This setting is suitable for a general living room. It
                reproduces the reverberation of sound just like in a movie
                theater (dubbing theater). It is most appropriate for watching
                content recorded on a Blu-ray Disc when you want the
                atmosphere of a movie theater
            "hdDcsStudio" - HD Digital Cinema Sound (HD-D.C.S.) Studio.
                This setting is suitable for a living room with the appropriate
                sound devices. It reproduces the reverberation of sound
                provided when a theatrical sound source is remixed for a
                Blu-ray Disc to a volume level suitable for home use.
            "proLogicII" - Dolby Pro Logic II Movie mode decoding.
                This setting is ideal for movies encoded in Dolby Surround.
            "proLogicIIx" - Dolby Pro Logic IIx Movie mode decoding.
                This setting expands Dolby Pro Logic II Movie or Dolby Digital
                5.1 to 7.1 discrete movie channels.
            "neo6Cinema" - DTS Neo:6 Cinema mode decoding.
                Sources recorded in 2-channel format are enhanced up to 7
                channels.
            "frontSurround" - An immersive virtual surround sound experience
                with only front speakers.
            "off" - Disable Sound Field Movie function.
        :rtype: str

        """
        return self.__send('soundFieldMovie')

    @sound_field_movie.setter
    def sound_field_movie(self, value):
        """
        Sets Sound Field Movie function.

        :param value: Possible values:
            "hdDcsDynamic" - HD Digital Cinema Sound (HD-D.C.S.) Dynamic.
                This setting is suitable for an environment which is
                reverberant but lacks a spacious feel (where sound absorption
                is not sufficient). It emphasizes the reflection of sound and
                reproduces the sound of a large, classic movie theater.
            "hdDcsTheater" - HD Digital Cinema Sound (HD-D.C.S.) Theater.
                This setting is suitable for a general living room. It
                reproduces the reverberation of sound just like in a movie
                theater (dubbing theater). It is most appropriate for watching
                content recorded on a Blu-ray Disc when you want the
                atmosphere of a movie theater
            "hdDcsStudio" - HD Digital Cinema Sound (HD-D.C.S.) Studio.
                This setting is suitable for a living room with the appropriate
                sound devices. It reproduces the reverberation of sound
                provided when a theatrical sound source is remixed for a
                Blu-ray Disc to a volume level suitable for home use.
            "proLogicII" - Dolby Pro Logic II Movie mode decoding.
                This setting is ideal for movies encoded in Dolby Surround.
            "proLogicIIx" - Dolby Pro Logic IIx Movie mode decoding.
                This setting expands Dolby Pro Logic II Movie or Dolby Digital
                5.1 to 7.1 discrete movie channels.
            "neo6Cinema" - DTS Neo:6 Cinema mode decoding.
                Sources recorded in 2-channel format are enhanced up to 7
                channels.
            "frontSurround" - An immersive virtual surround sound experience
                with only front speakers.
            "off" - Disable Sound Field Movie function.
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('soundFieldMovie', value=value)

    @property
    def night_mode(self):
        """
        Gets Night mode.

        Sound is output at low volume with minimum loss of fidelity and
        clarity of dialogue.

        :return: Possible values:
            True - "on", Enable Night mode.
            False - "off", Disable Night mode.
        :rtype: bool
        """
        return self.__send('nightMode')

    @night_mode.setter
    def night_mode(self, value):
        """
        Sets Night mode.

        Sound is output at low volume with minimum loss of fidelity and
        clarity of dialogue.

        :param value: Possible values:
            True - "on", Enable Night mode.
            False - "off", Disable Night mode.
        :type value: bool
        :return: None
        :rtype: None
        """
        self.__send('nightMode', value='on' if value else 'off')

    @property
    def night_mode_tmp(self):
        """
        Gets Night mode tmp.

        Sound is output at low volume with minimum loss of fidelity and
        clarity of dialogue.

        :return: Possible values:
            True - "on", Enable Night mode.
            False - "off", Disable Night mode.
        :rtype: bool
        """
        return self.__send('nightModeTmp')

    @night_mode_tmp.setter
    def night_mode_tmp(self, value):
        """
        Sets Night mode tmp.

        Sound is output at low volume with minimum loss of fidelity and
        clarity of dialogue.

        :param value: Possible values:
            True - "on", Enable Night mode.
            False - "off", Disable Night mode.
        :type value: bool
        :return: None
        :rtype: None
        """
        self.__send('nightModeTmp', value='on' if value else 'off')

    @property
    def pure_direct(self):
        """
        Gets Pure Direct function.

        When the Pure Direct function is on, the display panel lights off to
        suppress noise that affects sound quality.

        :return: Possible values:
            True - "on", Enable Pure Direct function.
            False - "off", Disable Pure Direct function.
        :rtype: bool
        """
        return self.__send('pureDirect')

    @pure_direct.setter
    def pure_direct(self, value):
        """
        Sets Pure Direct function.

        When the Pure Direct function is on, the display panel lights off to
        suppress noise that affects sound quality.

        :param value: Possible values:
            True - "on", Enable Pure Direct function.
            False - "off", Disable Pure Direct function.
        :type value: bool
        :return: None
        :rtype: None
        """
        self.__send('pureDirect', value='on' if value else 'off')

    @property
    def optimizer(self):
        """
        Gets Sound Optimizer function.

        Enjoying clear and dynamic sound at a low volume.

        :return: Possible values:
            "normal" - Normal mode. Adjusts for the reference level of a movie.
            "low" - Low mode. Adjusts for a CD or other software whose average
                sound pressure level is processed highly.
            "off" - Disable Sound Optimizer function.
        :rtype: str
        """
        return self.__send('optimizer')

    @optimizer.setter
    def optimizer(self, value):
        """
        Sets Sound Optimizer function.

        Enjoying clear and dynamic sound at a low volume.

        :param value: Possible values:
            "normal" - Normal mode. Adjusts for the reference level of a movie.
            "low" - Low mode. Adjusts for a CD or other software whose average
                sound pressure level is processed highly.
            "off" - Disable Sound Optimizer function.
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('optimizer', value=value)

    @property
    def calibration_type(self):
        """
        Gets Calibration type after you have performed the Auto Calibration
        and saved the settings.

        :return: Possible values:
            "fullFlat" - Full Flat. Makes the measurement of frequency from
                each speaker flat.
            "engineer" - Engineer. Sets to "the Sony listening room standard"
                frequency characteristics.
            "frontReference" - Front Reference. Adjusts the characteristics of
                all of the speakers to match the characteristics of the front
                speaker.
            "off" - Disable Calibration type.
        :rtype: str
        """
        return self.__send('calibrationType')

    @calibration_type.setter
    def calibration_type(self, value):
        """
        Sets Calibration type after you have performed the Auto Calibration
        and saved the settings.

        :param value: Possible values:
            "fullFlat" - Full Flat. Makes the measurement of frequency from
                each speaker flat.
            "engineer" - Engineer. Sets to "the Sony listening room standard"
                frequency characteristics.
            "frontReference" - Front Reference. Adjusts the characteristics of
                all of the speakers to match the characteristics of the front
                speaker.
            "off" - Disable Calibration type.
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('calibrationType', value=value)

    @property
    def voice(self):
        """
        Gets Voice mode.

        This helps make dialogues clearer.

        :return: Possible values:
            "type1" - Type 1. Standard.
            "type2" - Type 2. Dialogue range is enhanced.
            "type3" - Type 3. Dialogue range is enhanced, and the parts of
            range difficult to be discerned by the elderly are boosted.
        :rtype: str

        """
        return self.__send('voice')

    @voice.setter
    def voice(self, value):
        """
        Sets Voice mode.

        This helps make dialogues clearer.

        :param value: Possible values:
            "type1" - Type 1. Standard.
            "type2" - Type 2. Dialogue range is enhanced.
            "type3" - Type 3. Dialogue range is enhanced, and the parts of
            range difficult to be discerned by the elderly are boosted.
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('voice', value=value)

    @property
    def av_sync(self):
        """
        Gets the delay time (ms) of input audio to adjust Audio and Video Sync.

        Note that the range and step values vary depending on device.

        :return: Possible values are 0 (min) to 300 (max) stp by 25
        :rtype: int
        """
        return self.__send('avSyncMs')

    @av_sync.setter
    def av_sync(self, value):
        """
        Sets the delay time (ms) of input audio to adjust Audio and Video Sync.

        Note that the range and step values vary depending on device.

        :param value: Possible values are 0 (min) to 300 (max) stp by 25
        :type value: int
        :return: None
        :rtype: None
        """
        self.__send('avSyncMs', value=value)

    @property
    def dual_mono(self):
        """
        Gets Dual Mono mode.

        :return: Possible values:
            "main_sub" - Main/Sub mode. Sound in the main language will be
                output through the front left speaker and sound in the sub
                language will be output through the front right speaker
                simultaneously.
            "main" - Main mode. Sound in the main language will be output.
            "sub" - Sub mode. Sound in the sub language will be output.
        :rtype: str
        """
        return self.__send('dualMono')

    @dual_mono.setter
    def dual_mono(self, value):
        """
        Sets Dual Mono mode.

        :param value: Possible values:
            "main_sub" - Main/Sub mode. Sound in the main language will be
                output through the front left speaker and sound in the sub
                language will be output through the front right speaker
                simultaneously.
            "main" - Main mode. Sound in the main language will be output.
            "sub" - Sub mode. Sound in the sub language will be output.
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('dualMono', value=value)

    @property
    def wide_stereo(self):
        """
        Gets Wide Stereo mode for immersive stereo sound.

        :return: Possible values:
            "high" - Wide Stereo High mode.
            "standard" - Wide Stereo Standard mode.
        :rtype: str
        """
        return self.__send('wideStereo')

    @wide_stereo.setter
    def wide_stereo(self, value):
        """
        Sets Wide Stereo mode for immersive stereo sound.

        :param value: Possible values:
            "high" - Wide Stereo High mode.
            "standard" - Wide Stereo Standard mode.
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('wideStereo', value=value)

    @property
    def scene_selection(self):
        """
        Gets Custom Preset scene.

        Each preset scene saves various settings with the player, monitor,
        etc., according to listening and viewing style.

        :return: Possible values:
            "movie" - Movie scene.
            "music" - Music scene.
            "party" - Party scene.
            "night" - Night scene.
            "undo" - Undo custom preset scene settings.
            "" - Scene Selection Settings is Unknown.
        :rtype: str
        """
        return self.__send('sceneSelection')

    @scene_selection.setter
    def scene_selection(self, value):
        """
        Sets Custom Preset scene.

        Each preset scene saves various settings with the player, monitor,
        etc., according to listening and viewing style.

        :param value: Possible values:
            "movie" - Movie scene.
            "music" - Music scene.
            "party" - Party scene.
            "night" - Night scene.
            "undo" - Undo custom preset scene settings.
            "" - Scene Selection Settings is Unknown.
        :type value: str
        :return: None
        :rtype: None
        """
        self.__send('sceneSelection', value=value)

    @property
    def audio_pureness_control(self):
        """
        Gets whether changing screen to black to improve sound quality.

        :return: Possible Values
            True - "on", Enable APC function
            False - "off", Disable APC function
        :rtype: bool

        """
        return self.__send('audioPurenessControl')

    @audio_pureness_control.setter
    def audio_pureness_control(self, value):
        """
        Sets whether changing screen to black to improve sound quality.

        :param value: Possible Values
            True - "on", Enable APC function
            False - "off", Disable APC function
        :type value: bool
        :return: None
        :rtype: None

        """
        self.__send(
            'audioPurenessControl',
            value='on' if value else 'off'
        )

    @property
    def audio_pureness_control_tmp(self):
        """


        :return: Possible Values
            True - "on", Enable APC function
            False - "off", Disable APC function
        :rtype: bool

        """
        return self.__send('audioPurenessControlTmp')

    @audio_pureness_control_tmp.setter
    def audio_pureness_control_tmp(self, value):
        """


        :param value: Possible Values
            True - "on", Enable APC function
            False - "off", Disable APC function
        :type value: bool
        :return: None
        :rtype: None

        """
        self.__send(
            'audioPurenessControlTmp',
            value='on' if value else 'off'
        )
