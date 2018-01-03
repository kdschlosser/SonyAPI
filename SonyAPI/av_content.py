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
from . import singleton, container
from .exception import ContentProtectedError



class ExternalTerminal(object):
    # noinspection PyPep8Naming
    def __init__(
        self,
        sony_api,
        uri
    ):
        self.__icon_url = None
        self.__meta = None
        self.__outputs = None
        self.__label = None
        self.__active = None
        self.__connection = None
        self.__title = None
        self.__uri = uri
        self.__sony_api = sony_api

    def __send(self, method, **params):
        return self.__sony_api.send('avContent', method, **params)

    @property
    def icon_url(self):
        """
        Gets the icon URL that the service uses for the terminal.

        :return: URL
        :rtype: str
        """
        self.__update()
        return self.__icon_url

    @property
    def meta(self):
        """
        Gets describes the type of terminal.

        For example, this can provide a hint to an application as to which
        icon to show to the user. The type is provided using a "meta" URI
        format. Your application should customize its UI based on the type of
        the terminal, such as choosing an appropriate image.

        :return: Possible values:
            "" - No meta information is available for this terminal
            "meta:audiosystem" - An audio system type CEC device is connected
                to the terminal
            "meta:avamp" - An AV amplifier is connected to the terminal
            "meta:bd-dvd" - BD/DVD input
            "meta:btaudio" - Bluetooth audio input
            "meta:btphone" - BT phone input
            "meta:camcoder" - A video camera is connected to the terminal
            "meta:coaxial" - Coaxial digital audio input
            "meta:complex" - A complex device is connected to the terminal
            "meta:component" - Component input (Y and Pb/Cb and Pr/Cr
                connectors)
            "meta:componentd" - D-Component input
            "meta:composite" - Composite input
            "meta:composite_componentd" - Composite and D-Component combined
                input
            "meta:digitalcamera" - A digital camera is connected to the
                terminal
            "meta:disc" - A disk player is connected to the terminal
            "meta:dsub15" - D-subminiature 15pin input
            "meta:game" - A game console is connected to the terminal
            "meta:hdmi" - HDMI input
            "meta:hdmi:output" - HDMI output
            "meta:hometheater" - A home theater device is connected to the
                terminal
            "meta:line" - Axillary input
            "meta:linemini" - A mini audio port, the exact hardware port is
                device dependent
            "meta:optical" - Optical digital audio input
            "meta:pc" - A personal computer is connected to the terminal
            "meta:playbackdevice" - A playback type CEC device is connected to
                the terminal
            "meta:recordingdevice" - A recording type CEC device is connected
                to the terminal
            "meta:scart" - SCART input
            "meta:svideo" - S-Video input
            "meta:tape" - A tape player is connected to the terminal
            "meta:tuner" - A tuner is connected to the terminal
            "meta:tunerdevice" - A tuner type CEC device is connected to the
                terminal
            "meta:tv" - A TV type CEC device is connected to the terminal
            "meta:usbdac" - USB DAC input
            "meta:wifidisplay" - WiFi Display input
            "meta:wirelessTransceiver:output" - Wireless transceiver
            "meta:source" - Source input
            "meta:sacd-cd" - SACD/CD input
            "meta:sat-catv" - SAT/CATV input
            "meta:video" - Video input
            "meta:zone:output" - Zone output
        :rtype: str
        """
        self.__update()
        return self.__meta

    @property
    def outputs(self):
        """
        An array of the URIs of the output terminals that are available for
        this input terminal.

        :return: list of URI's
        :rtype: list
        """
        self.__update()
        return self.__outputs

    @property
    def label(self):
        """
        Gets the label that the user assigned to this terminal.

        :return: Example: "Game"
        :rtype: str
        """
        self.__update()
        return self.__label

    @property
    def active(self):
        """
        Gets active status of the terminal.

        For a terminal type of "meta:zone:output", the active status indicates
        whether the zone is enabled. For all other terminal types, the active
        status indicates whether the source is selected as an input source for
        any output zone.

        :return: Possible values:
            None - The active status could not be determined.
            True - "active", The terminal is enabled or a selected input
                source.
            False - "inactive" - The terminal is disabled or not a selected
                input source.
        :rtype: bool, None
        """
        self.__update()
        return (
            True if self.__active == 'active' else
            False if self.__active == 'inactive' else
            None
        )

    @active.setter
    def active(self, value):
        """
        Sets this terminal as active.

        :param value: Possible values:
            True - "active", Terminal is active.
            False - "inactive", Terminal is inactive
        :type value: bool
        :return: None
        :rtype: None
        """
        self.__send(
            'setActiveTerminal',
            active='active' if value else 'inactive',
            uri=self.uri
        )

    @property
    def is_connected(self):
        """
        Gets the connection status of the terminal.

        :return: Possible values:
            True - "connected", The terminal is connected.
            False - "unconnected", The terminal is not connected.
            None - "unknown", The connection status is unknown.
        :rtype: bool, None
        """
        self.__update()
        return (
            True if self.__connection == 'connected' else
            False if self.__connection == 'unconnected' else
            None
        )

    @property
    def title(self):
        """
        Gets the name of the input or output terminal.

        :return: Examples:
            "HDMI 2"
            "Component 1"
        :rtype: str
        """
        self.__update()
        return self.__title

    @property
    def uri(self):
        """
        Gets the URI of the external terminal.
        :return: Example: "extInput:hdmi?port=2"
        :rtype: str
        """
        return self.__uri

    @property
    def playing_content(self):
        playing_content = self.__send(
            'getPlayingContentInfo',
            output=self.uri
        )[0]
        playing_content['output'] = self

        if 'source' in playing_content and playing_content['source']:
            scheme_name, source_name = playing_content['source'].split(':')
            scheme = getattr(self.__sony_api.av_content, scheme_name)
            source = getattr(scheme, source_name)
            playing_content['source'] = source

        return ContentItem(sony_api=self.__sony_api, **playing_content)

    def pause(self):
        """
        Pauses playing content.

        :return: None
        :rtype: None

        """
        self.__send('pausePlayingContent', output=self.uri)

    def scan_forward(self):
        """
        Fast Forward playing content.

        :return: None
        :rtype: None
        """
        self.__send('scanPlayingContent', direction='fwd', output=self.uri)

    def scan_backwards(self):
        """
        Rewind playing content.

        :return: None
        :rtype: None
        """
        self.__send('scanPlayingContent', direction='bwd', output=self.uri)

    def stop(self):
        """
        Stop playing content.

        :return: None
        :rtype: None
        """

        self.__send('stopPlayingContent', output=self.uri)

    def play_next(self):
        """
        Skip to next content in queue.

        :return: None
        :rtype: None
        """
        self.__send('setPlayNextContent', output=self.uri)

    def play_previous(self):
        """
        Skip to previous content in queue.

        :return: None
        :rtype: None
        """
        self.__send('setPlayPreviousContent', output=self.uri)

    def __update(self):
        terminals = self.__send('getCurrentExternalTerminalsStatus')[0]
        for terminal in terminals:
            if terminal['uri'] == self.uri:
                self.__icon_url = terminal['iconUrl']
                self.__meta = terminal['meta']
                self.__outputs = terminal['outputs']
                self.__label = terminal['label']
                self.__active = terminal['active']
                self.__connection = terminal['connection']
                self.__title = terminal['title']
                self.__uri = terminal['uri']
                break
        else:
            raise AttributeError


class PlaybackMode(object):
    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, method, **params):
        return self.__sony_api.send('avContent', method, **params)

    @property
    def auto_playback(self):
        """

        :return: Possible values:
            True - "on", Auto playback mode enabled.
            False = "off", Auto playback mode disabled.
        :rtype: bool
        """
        return self.__send(
            'getPlaybackModeSettings',
            target='autoPlayback'
        )[0]['currentValue'] == 'on'

    @property
    def play_type(self):
        """
        Gets the playback mode

        :return: Possible values:
            "normal" - Normal playback
            "folder" - Playback enabled for a unit of folder and its sub
                folder.
            "repeatAll" - In case current composed of multiple parts, repeat
                playback enabled for whole parts.
            "repeatFolder" - Repeat playback enabled for a unit of folder and
            its sub folder.
            "repeatTrack" - Repeat playback enabled for a unit of track (audio
                content) or title (video content).
            "shuffleAll" - In case current composed of multiple parts, shuffle
                playback enabled for whole parts.
        :rtype: str
        """
        return self.__send(
            'getPlaybackModeSettings',
            target='playType'
        )[0]['currentValue']

    @play_type.setter
    def play_type(self, value):
        """
        Sets the playback mode.

        :param value: Allowed values:
            "normal" - Normal playback
            "folder" - Playback enabled for a unit of folder and its sub folder
            "repeatAll" - In case current composed of multiple parts, repeat
                playback enabled for whole parts.
            "repeatFolder" - Repeat playback enabled for a unit of folder and
                its sub folder.
            "repeatTrack" - Repeat playback enabled for a unit of track (audio
                content) or title (video content).
            "shuffleAll" - In case current composed of multiple parts, shuffle
                playback enabled for whole parts.
        :return: None
        :rtype: None
        """

        self.__send(
            'setPlaybackModeSettings',
            settings=[dict(target='playType', value=value)]
        )

    @property
    def repeat_type(self):
        """
        Gets the repeat mode.

        :return: Possible values:
            "all" - In case current composed of multiple parts, repeat
                playback enabled for whole parts.
            "folder" - Repeat playback enabled for a unit of folder and its
                sub folder.
            "track" - Repeat playback enabled for a unit of track (audio
                content) or title (video content).
            "chapter" - Repeat playback enabled for a unit of chapter.
            "off" - Repeat playback disabled as a device setting.
        :rtype: str
        """
        return self.__send(
            'getPlaybackModeSettings',
            target='repeatType'
        )[0]['currentValue']

    @repeat_type.setter
    def repeat_type(self, value):
        """
        Sets the repeat mode.

        :param value: Allowed values:
            "all" - In case current composed of multiple parts, repeat
                playback enabled for whole parts.
            "folder" - Repeat playback enabled for a unit of folder and its
                sub folder.
            "track" - Repeat playback enabled for a unit of track (audio
                content) or title (video content).
            "chapter" - Repeat playback enabled for a unit of chapter.
            "off" - Repeat playback disabled as a device setting.
        :return: None
        :rtype: None
        """

        self.__send(
            'setPlaybackModeSettings',
            settings=[dict(target='repeatType', value=value)]
        )

    @property
    def shuffle_type(self):
        """
        Gets the shuffle mode.

        :return: Possible values:
            "folder" - Shuffle of a unit of folder and its sub folder. of file
                name.
            "off" - Shuffle playback disabled as a device setting.
        :rtype: str
        """
        return self.__send(
            'getPlaybackModeSettings',
            target='shuffleType'
        )[0]['currentValue']

    @shuffle_type.setter
    def shuffle_type(self, value):
        """
        Sets the shuffle mode.

        :param value: Allowed values:
            "folder" - Shuffle of a unit of folder and its sub folder. of file
                name.
            "off" - Shuffle playback disabled as a device setting
        :return: None
        :rtype: None
        """

        self.__send(
            'setPlaybackModeSettings',
            settings=[dict(target='shuffleType', value=value)]
        )


class ContentItem(object):
    """
    Class that represents a piece of content on a Sony Device.

    This is a tricky class due to the large number of variations it can have.
    It all depends on the model of the device as well as the device type. Also
    the supported features of the device play into it as well.

    I will do my best to explain.

    This class can be passed any number of different variables/variable
    combinations when it is created. Because of this I have elected to use a
    dynamic system of adding these variables. I have altered the output of
    dir() to show the different variables that have been added. if a variable
    has not been added it will not show in the output of dir() as well as it
    will raise an AttributeError if you try to get a variable that has not been
    added. setting of any of these variables is not allowed and will raise an
    AttributeError if you try to, unless there is a property for that variable
    that has a setter that has been hard coded.

    depending on the source of the content item is going to affect which
    variables are available. Below are 3 different source types and then the
    list of variables. If a variables is attached to a specific source type it
    will be noted next to the variable name.


    storage:
        "storage:internalHdd" - Internal HDD storage for content.
        "storage:memoryCard1" - Memory card1 for content.
        "storage:memoryCard2" - Memory card2 for content.
        "storage:usb1" - USB1 storage for content.
        "storage:usb2" - USB2 storage for content.
        "usb:massStorage" - USB storage for media files.
        "usb:recStorage" - USB storage for recording TV broadcasting program

    TV type 1:
        "tv:antenna" - ATSC terrestrial tuner resource
        "tv:cable" - ATSC cable tuner resource
        "tv:dvbc" - DVB cable tuner resource
        "tv:dvbs" - DVB satellite tuner resource
        "tv:dvbsj" - Japan DVB-based communication Satellite tuner resource
        "tv:dvbt" - DVB terrestrial tuner resource
        "tv:isdbbs" - ISDB BS satellite tuner resource
        "tv:isdbcs" - ISDB CS satellite tuner resource
        "tv:isdbgt" - ISDBG terrestrial tuner resource (BR region)
        "tv:isdbt" - ISDB terrestrial tuner resource

    TV type 2:
        "tv:isdbbs" - ISDB BS satellite tuner resource
        "tv:isdbcs" - ISDB CS satellite tuner resource
        "tv:isdbt" - ISDB terrestrial tuner resource

    TV type 3:
        "tv:antenna" - ATSC terrestrial tuner resource
        "tv:cable" - ATSC cable tuner resource
        "tv:isdbgt" - ISDBG terrestrial tuner resource (BR region)

    Examples of some of the different content variables:
        disp_num: User friendly channel number.
            TV type 1
            example values:
                "101", "211.2"

        original_disp_num: Original display number.:
            TV type 1

        triplet_str: Triplet string to identify channel.
            TV type 1
            Value example:
                "11.22.33"

        program_num: Program number on broadcasting data table.
            TV type 1

        program_media_type: Media type of broadcast program.
            TV type 1
            Example values:
                "tv" - means TV program
                "radio" - means radio program
                "data" - means data program
                "" - unknown type

        direct_remote_num: Mapped number button on remote controller.
            TV type 1
            Example values:
                int(1 through 12)

        epg_visibility: Getting the visibility on EPG application.
            TV type 2
            Example values:
                "visible" - This content is shown in EPG.
                "invisible" - This content is hidden in EPG.
                "auto" - This content is shown if this content is main channel
                    in EPG.

        channel_surfing_visibility: Getting the visibility on pushing
            <Channel+> / <Channel-> button.
            TV type 2
            Example values:
                "visible" - This content is shown.
                "invisible" - This content is hidden.

        visibility: Media type of broadcast program.
            TV type 3
            Example values:
                "visible" - This content is shown.
                "invisible" - This content is hidden.

        start_date_time: Scheduled date and time to start.
            storage
            Example values:
                ISO-8601 time format YYYY-MM-DDTHH:MM:SS.sTZD.

        channel_name: Broadcaster channel name of the recorded content.
            storage
            Example values:
                "NBC", "ABC", "FOX", "HBO"

        file_size_byte: File size of the content in bytes.
            storage
            Example values:
                int(1024)

        is_already_played: Gets if the content been played.
            storage
            Example values:
                True - already played
                False - not played yet

        duration_sec: Duration in seconds.
            storage
            Example values:
                int(300) (5 minutes)

        user_content_flag: No information

        created_time: No information

        sizeMb: No information

        parental_country: No information

        parental_system: No information

        parental_rating: No information

        subtitle_title: No information

        subtitle_language: No information

        audio_channel: No information

        audio_frequency: No information

        audio_codec: No information

        chapter_count: No information

        video_codec: No information

        storage_uri: No information

        product_id: No information

        idx: No information

        status: No information

    The following variables are available when using this API with a
    home audio device.

        application_name: The name of the application that is playing the
            content, or null or omitted if it is undefined. If the content is
            streaming via the Cast for Audio service, the name of the casted
            application is used.

        service: The URI for service information if the device is playing
            network service content; otherwise "". You can use this URI to
            retrieve service information about the playing content.

        content_kind: Identifies the content type.
            Possible values:
                "" - Unknown
                "directory" - Directory
                "input" - External input
                "movie" - Movie
                "movie_avi" - AVI movie
                "movie_mp4" - MP4 movie
                "movie_xavcs" - XAVC S movie
                "music" - Music
                "radio" - Radio
                "service" - Network service
                "still" - Still image
                "still_group" - Still group

        album_name: The Album name for the content, or null or omitted if no
            album name is defined.

        artist: The artist's name, or null or omitted if no artist name is
            defined.

        state_info: The playback status of the device. If a value for this
            field is included in the notification, at least one of its fields
            will contain a value.
            The returned value of this wil be a Container instance

        output: instance of ExternalTerminal.

        parent_uri: The URI of the parent directory if the source is browsable;
            otherwise "".

        dab_info: Digital Audio Broadcasting ( DAB ) information for the
            playing content. If a value for this field is included in the
            notification, at least one of its fields will contain a value.
            The returned value of this wil be a Container instance

        broadcast_freq_band: The broadcast frequency band for the content.
            Possible values:
                "" - No band data
                "am" - AM
                "fm" - FM
                "lw" - LW
                "mw" - MW
                "sw" - SW
        broadcast_freq: The broadcast frequency for the content, in Hz.
            Example: float(105.9)

        total_count: The number of content items in the playback scope.

        file_no: The file number of the content. What a file represents depends
            on the content type, such as a track or a broadcast preset item.

        video_info: Video information for the playing content. If a value for
            this field is included in the notification, at least one of its
            fields will contain a value.
            The returned value of this wil be a Container instance

        index: The index of the content list.

        audio_info: Audio information for the playing content. If a value for
            this field is included in the notification, at least one of its
            fields will contain a value.
            The returned value of this wil be a Container instance

        podcast_name: The name of the podcast, or null or omitted if this
            content is not from a podcast.

        playlist_name: The name of the playlist in which the content is
            included, or null or omitted if no playlist is defined.

        genre: The genres assigned to the content, or null or omitted if no
            genres are assigned. This is used for display purpose and is
            device-dependent.

        duration_msec: The length of the content, in milliseconds.

        position_msec: The playing position within the content, in
            milliseconds.

        source_label: The display name of the source of the playing content.

        play_speed: The current play speed, expressed as a number with one
            decimal place.
            Example values:
                "1.0"
                "1.5"

        media_type: The media type of the playing content.
            Possible values:
                "" - unknown type
                "audio" - audio(music) content
                "image" - image(photo) content
                "video" - video content

        repeat_type: The repeat setting for the current content.
            "off" - Repeat playback disabled for the single unit of content
                currently playing.
            "on" - Repeat playback enabled for the single unit of content
                currently playing.

        play_speed_step: The playback speed setting of the content. Positive
            numbers represent fast-forward settings, with greater numbers
            representing faster speeds. Negative numbers represent slow-motion
            settings, with lesser numbers representing slower speeds. The
            playback speed for each setting is device dependent.
            Possible values:
                3 - Fast forward
                2 - Fast forward
                1 - Fast forward
                0 - Normal speed
                -1 - Slow motion
                -2 - Slow motion
                -3 - Slow motion

        position_sec: Deprecated for unit consistency with other APIs. The
            playing position within the content, in seconds.


    And that is what I have so far. If you have any further information please
    feel free to add to this doc and submit the changes to
    https://github.com/kdschlosser/SonyAPI
    """
    __metaclass__ = singleton.Singleton

    def __init__(
        self,
        source,
        sony_api,
        uri,
        title,
        index,
        **kwargs
    ):
        self.__uri = uri
        self.__title = title
        self.__index = index
        self.__source = source
        self.__sony_api = sony_api

        self.__variables = dict()

        for key in kwargs.keys():
            attr_name = '_'
            for char in key:
                if char.isupper():
                    attr_name += '_'
                attr_name += char.lower()

            while attr_name[-1] == '_':
                attr_name = attr_name[:-1]

            self._variables[attr_name] = kwargs[key]

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if '_' + item in self._variables:
            attr = self.__variables['_' + item]

            if isinstance(attr, dict):
                return container.Container(**attr)
            return attr

        raise AttributeError

    def __setattr__(self, key, value):
        if (
            key == '__variables' or
            (
                key.startswith('_') and
                '_' + key not in self.__variables
            )
        ):
            object.__setattr__(self, key, value)
        else:
            raise AttributeError

    def __send(self, method, **params):
        return self.__sony_api.send('avContent', method, **params)

    @property
    def source(self):
        return self.__source

    @property
    def uri(self):
        """
        URI to identify the content item.

        :return: URI, (ex) "tv:isdbt?trip=11.22.33"
        :rtype: str
        """
        return self.__uri

    @property
    def title(self):
        """
        Title of this content item.

        :return: Title, (ex) "Sports Channel"
        :rtype: str
        """
        return self.__title

    @property
    def index(self):
        """
        Index of this item in the content list gotten from the source.

        :return: Source content index.
        :rtype: int
        """
        return self.__index

    @property
    def is_protected(self):
        """
        Gets if the content item is protected from deletion.

        This property is only available for the following sources:
            "storage:internalHdd" - Internal HDD storage for content.
            "storage:memoryCard1" - Memory card1 for content.
            "storage:memoryCard2" - Memory card2 for content.
            "storage:usb1" - USB1 storage for content.
            "storage:usb2" - USB2 storage for content.
            "usb:massStorage" - USB storage for media files. (Use in limited
                methods)
            "usb:recStorage" - USB storage for recording TV broadcasting
                program

        :returns: Possible values:
            True - Item is protected
            False - Item is not protected
        :rtype: bool
        :raise: AttributeError if the source is not one of the above.
        """
        if '_is_protected' not in self.__variables:
            raise AttributeError

        return self.__variables['_is_protected']

    @is_protected.setter
    def is_protected(self, value=False):
        """
        Sets this content item so it cannot be deleted.

        This property is only available for the following sources:
            "storage:internalHdd" - Internal HDD storage for content.
            "storage:memoryCard1" - Memory card1 for content.
            "storage:memoryCard2" - Memory card2 for content.
            "storage:usb1" - USB1 storage for content.
            "storage:usb2" - USB2 storage for content.
            "usb:massStorage" - USB storage for media files. (Use in limited
                methods)
            "usb:recStorage" - USB storage for recording TV broadcasting
                program

        :param value: Possible values:
            True - Item is protected
            False - Item is not protected

        :type value: bool
        :return: None
        :rtype: None
        :raise: AttributeError if the source is not one of the above.
        """
        if '_is_protected' not in self.__variables:
            raise AttributeError

        self.__variables['_is_protected'] = value
        self.__send('setDeleteProtection', uri=self.uri, isProtected=value)

    def delete(self):
        """
        Deletes this content item:

        :return: None
        :rtype: None
        :raise:
            AttributeError: If method is not supported
            ContentProtectedError: If is_protected is True
        """
        if '_is_protected' not in self.__variables:
            raise AttributeError

        if self.__variables['_is_protected'] is True:
            raise ContentProtectedError([
                41000,
                'This content item is protected from deletion'
            ])

        self.__send('deleteContent', uri=self.uri)

    def play(self, zone=None):
        """
        Plays this content item.

        :param zone: Zone number.
            Only used if the device is a multi zone device.
        :type zone: int
        :return: None
        :rtype: None
        """

        interface_info = self.__sony_api.system.interface_information

        if interface_info.product_category not in ('tv', 'camera'):
            if zone is not None:
                zone = 'extOutput:zone?zone=' + str(zone)
                self.__send('setPlayContent', uri=self.uri, output=zone)
                return

        self.__send('setPlayContent', uri=self.uri)


class SchemeItem(object):
    __metaclass__ = singleton.Singleton

    def __init__(self, sony_api, name):
        self.__sony_api = sony_api
        self.__name = name.replace('_', '-')

        self.__name__ = ''
        for item in name.split('_'):
            self.__name__ += item[0].upper() + item[1:]

    def __send(self, method, **params):
        return self.__sony_api.send('avContent', method, **params)

    @property
    def name(self):
        return self.__name

    @property
    def sources(self):
        """
        Gets source list.

        This retrieves a list of available source URI's so you are able to
        display the available source items to the user.

        For control purposes you will want to access the source item like it
        is a variable of the instance of this scheme.

        You will want to replace "-" with an "_" this will return an instance
        of SonyAPI.av_content.Source that represents the Source. If there is a
        specific port or content item that is attached to a source item then
        you will need to request that resource from that instance in the same
        manner.

        examples of the various source items prefix with a * shows examples of
        the above.


        av_content = SonyAPI(instance).av_content


        *** TV sources ***
        tv = av_content.tv

            "antenna" - ATSC terrestrial tuner resource
            * tv.antenna
            "cable" - ATSC cable tuner resource
            * tv.cable
            "dvbc" - DVB cable tuner resource
            * tv.dvbc
            "dvbs" - DVB satellite tuner resource
            * tv.dvbs
            "dvbsj" - Japan DVB-based communication Satellite tuner resource
            * tv.dvbsj
            "dvbt" - DVB terrestrial tuner resource
            * tv.dvbt
            "isdbbs" - ISDB BS satellite tuner resource
            * tv.isdbbs
            "isdbcs" - ISDB CS satellite tuner resource
            * tv.isdbcs
            "isdbgt" - ISDBG terrestrial tuner resource (BR region)
            * tv.isdbgt
            "isdbt" - ISDB terrestrial tuner resource
            * tv.isdbt


        *** External Inputs ***
        extInput = av_content.extInput

            "airPlay" - AirPlay input resource
            * extInput.airPlay
            "bd-dvd" - BD/DVD input resource
            * extInput.bd_dvd
            "btAudio" - Bluetooth Audio input resource
            * extInput.btAudio
            "cec" - CEC input resource
            * extInput.cec
            "coaxial" - Audio Coaxial input resource
            * extInput.coaxial
            "component" - Component external input resource
            * extInput.component
            "composite" - Composite external input resource
            * extInput.composite
            "dsub" - DSub input resource
            * extInput.dsub
            "game" - Game input resource
            * extInput.game
            "hdmi" - HDMI external input resource
            * extInput.hdmi
            "line" - Audio line input resource
            * extInput.line
            "optical" - Audio Optical input resource
            * extInput.optical
            "sacd-cd" - SACD/CD input resource
            * extInput.sacd_cd
            "sat-catv" - SAT/CATV input resource
            * extInput.sat_catv
            "scart" - SCART external input resource
            * extInput.scart
            "source" - Source input resource.
                This means that input resource is current main Zone input
                signal.
            * extInput.source
            "tv" - TV input resource
            * extInput.tv
            "usbDac" - USB DAC input resource
            * extInput.usbDac
            "video" - Video input resource
            * extInput.video
            "widi" - Wi-fi Display resource
            * extInput.widi


        *** USB ***
        usb = av_content.usb

            "massStorage" - USB storage for media files.
            * usb.massStorage
            "usb:recStorage" - USB storage for recording TV broadcasting
                program
            * usb.recStorage


        *** IPTV ***
        iptv = av_content.iptv

            "bivl" - BIVL movie/music resource.
            * iptv.bivl


        *** DLNA ***
        dlna = av_content.dlna

            "dlna:" - DLNA movie/music/photo resource.
            * dlna
            "music" - DLNA music resource.
            * dlna.music
            "movie" - DLNA movie resource.
            * dlna.movie
            "photo" - DLNA photo resource.
            * dlna.photo


        *** Video ***
        video = av_content.video

            "content" - Video content resource
            * video.content


        *** Audio ***
        audio = av_content.audio

            "content" - Audio content resource
            * audio.content


        *** Image ***
        image = av_content.image

            "content" - Image content resource
            * image.content


        *** External Output ***
        extOutput = av_content.extOutput

            "hdmi" - HDMI external output resource
            * extOutput.hdmi
            "wirelessTransceiver" - Wireless Transceiver external output
                resource
            * extOutput.wirelessTransceiver
            "zone" - Zone external output resource.
                You can enjoy audio at the same time in another room by
                connecting the speakers that are located in another room, which
                is identified by zone.
            * extOutput.zone


        *** Storage ***
        storage = av_content.storage

            "bd" - BD resource
            * storage.bd
            "cd" - CD resource
            * storage.cd
            "dvd" - DVD resource
            * storage.dvd
            "internalHdd" - Internal HDD storage for content.
            * storage.internalHdd
            "memoryCard1" - Memory card1 for content.
            * storage.memoryCard1
            "memoryCard2" - Memory card2 for content.
            * storage.memoryCard2
            "usb1" - USB1 storage for content.
            * storage.usb1
            "usb2" - USB2 storage for content.
            * storage.usb2

        *** Fav ***
        fav = av_content.fav

            "tv" - TV contents' managing favorite resources
                4 lists are managed.
            * fav.tv

        *** Radio ***
        radio = av_content.radio

            "am" - AM radio resource
            * radio.am
            "dab" - DAB radio resource
            * radio.dab
            "fm" - FM radio resource
            * radio.fm

        *** Net Service ***
        netService = av_content.netService

            "audio" - Audio Network service resource
            * netService.audio


        *** Cast ***
        cast = av_content.cast

            "audio" - Cast for Audio service resource
            * cast.audio


        *** Multiroom for Audio ***
        multiroom = av_content.multiroom

            "audio" - Multiroom for Audio service resource
            * multiroom.audio


        *** HDRL Movie ***
        hdrl = av_content.hdrl

            "movie" - HDRL Movie resource
            * hdrl.movie

        :return: List of available sources for a specific scene.
        :rtype: list
        """

        res = []
        interface_info = self.__sony_api.system.interface_information

        def process_source(src):
            src = src.split('?')[0]
            if src not in res:
                res.append(source)

        if interface_info.product_category == 'tv':
            sources = self.__send('getSourceList', scheme=self.name)[0]
            for source in sources:
                _, source = source['source'].split(':')
                process_source(source)

        elif interface_info.product_category != 'camera':
            res = []
            terminals = self.__send('getCurrentExternalTerminalsStatus')[0]
            for terminal in terminals:
                scheme, source = terminal['uri'].split(':')
                if self.name == scheme:
                    process_source(source)

        return res

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item.replace('_', '-') in self.sources:
            return SourceItem(self, self.__sony_api, item)
        raise AttributeError

    def __getitem__(self, item):
        try:
            return getattr(self, item.replace('-', '_'))
        except AttributeError:
            raise KeyError


class SourceItem(object):
    __metaclass__ = singleton.Singleton

    def __init__(self, source, sony_api, name):
        self.__sony_api = sony_api
        self.__name = name
        self.__source = source

        self.__name__ = ''

        for item in name.split('='):
            self.__name__ += item[0].upper() + item[1:]

        if self.__sony_api.device_type in ('tv', 'camera'):
            self.__available_outputs = None

            'scheme:source'

        else:
            self.__available_outputs = []
            terminals = self.__send('getCurrentExternalTerminalsStatus')[0]
            for terminal in terminals:

                uri = terminal['uri'].split('?')

                if len(uri) == 1:
                    continue
                if uri[1]



class Source(object):
    __metaclass__ = singleton.Singleton

    def __init__(self, scheme, sony_api, name):
        self.__sony_api = sony_api
        self.__name = name.replace('_', '-')
        self.__scheme = scheme
        self.__uri = scheme.name + ':' + self._name

        self.__name__ = ''
        for item in name.split('_'):
            self.__name__ += item[0] + item[1:]










    @property
    def uri(self):
        return self.__uri

    @property
    def name(self):
        return self.__name

    @property
    def scheme(self):
        return self.__scheme

    def __send(self, method, **params):
        return self.__sony_api.send('avContent', method, **params)

    def favorite_content(self, contents=('',)):
        self.__send(
            'setFavoriteContentList',
            favSource=self.uri,
            contents=list(contents)
        )

    favorite_content = property(fset=favorite_content)

    @property
    def content_count(self):
        return self.__send('getContentCount', source=self.uri)[0]['count']

    @property
    def output(self):
        if self.__sony_api.device_type in ('tv', 'camera'):
            raise AttributeError
        return self.__output

    @output.setter
    def output(self, value):
        if self.__sony_api.device_type in ('tv', 'camera'):
            raise AttributeError


    @property
    def playing_content(self):
        if self.__sony_api.idevice_type == 'tv':
            return ContentItem(
                self,
                self.__sony_api, **self.__send('getPlayingContentInfo')[0]
            )
        else:
            raise AttributeError

    @property
    def content(self):
        items = self.__send(' getContentList ', source=self.uri)[0]
        i = 50
        contents = []
        while items:
            contents += items
            items = self.__send(
                'getContentList',
                source=self.uri,
                stIdx=i
            )[0]
            i += 50

        return list(
            ContentItem(self, self.__sony_api, **content)
            for content in contents
        )

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        contents = self.content

        if item.startswith('port') or item.startswith('zone'):
            content_item = item[:4] + '=' + item[4:]
        elif self.name == 'cec':
            content_item = 'type='
            for char in item:
                if char.isdigit() and '&port' not in content_item:
                    content_item += '&port='
                content_item += char
        else:
            content_item = item

        content_item = content_item.replace('_', ' ')

        for content in contents:
            if content_item in (content.title, content.uri):
                return content
            if content_item in getattr(content, 'channel_name', ''):
                return content
        raise AttributeError

    def __getitem__(self, item):
        try:
            return getattr(self, item.replace(' ', '_'))
        except AttributeError:
            raise KeyError


class AVContent(object):

    def __init__(self, sony_api):
        self.__sony_api = sony_api
        self.__parental_ratings = None
        self.__tuner = None
        self.__playback_mode = None

    def __send(self, method, **params):
        return self.__sony_api.send('avContent', method, **params)

    @property
    def playback_mode(self):
        if self.__playback_mode is None:
            self.__playback_mode = PlaybackMode(self.__sony_api)
        return self.__playback_mode

    @property
    def tuner(self):
        if self.__tuner is None:
            self.__tuner = Tuner(self.__sony_api)
        return self.__tuner

    @property
    def __schemes(self):
        """
        Gets schemes.

        :return: Possible values:
            "tv" - Tuner resources
            "extInput" - External inputs resources
            "usb" - USB files resources
            "iptv" - IPTV movie/music resources. (Use in limited methods)
            "dlna" - DLNA files resources. (Use in limited methods)
            "video" - Video content resources
            "audio" - Audio content resources
            "image" - Image content resources
            "extOutput" - External outputs resources
            "storage" - Storage media resources
            "fav" - Favorite contents managing resources
            "radio" - radio contents resources
            "netService" - network service resources
            "cast" - cast service resources
            "multiroom" - multiroom resources
            "hdrl" - HDRL resources
        :rtype: list
        """
        interface_info = self.__sony_api.system.interface_information

        if interface_info.product_category == 'tv':
            return self.__send('getSchemeList')[0]

        elif interface_info.product_category != 'camera':
            res = []
            terminals = self.__send('getCurrentExternalTerminalsStatus')[0]
            for terminal in terminals:
                scheme = terminal['uri'].split(':')[0]
                if scheme not in res:
                    res += [scheme]
            return res

    @property
    def parental_ratings(self):

        if self.__parental_ratings is None:
            self.__parental_ratings = ParentalRatings(self.__sony__api)

        return self.__parental_ratings

    def pause(self):
        """
        Pauses all content on all outputs.

        :return: None
        :rtype: None

        """
        self.__send('pausePlayingContent')

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if not item.startswith('_'):
            if item.replace('_', '-') in self.__schemes:
                return SchemeItem(self.__sony_api, item)

        raise AttributeError

    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        else:
            raise AttributeError


class Tuner(object):

    def __init__(self, sony_api):
        self.__sony_api = sony_api
        self.__auto_tune = True

    def __send(self, direction):

        self.__sony_api.send(
            'avContent',
            'seekBroadcastStation',
            tuning='auto' if self.__auto_tune else 'manual',
            direction=direction
        )

    @property
    def auto_tune(self):
        """
        Gets tuning mode.

        :return: Possible values:
            True - "auto", Automatic tuning enabled.
            False - "manual", Manual tuning enabled.
        :rtype: bool
        """
        return self.__auto_tune

    @auto_tune.setter
    def auto_tune(self, value):
        """
        Sets the tuning mode.

        :param value: Allowed values:
            True - "auto", Automatic tuning enabled.
            False - "manual", Manual tuning enabled.
        :type value: bool
        :return: None
        :rtype: None
        """
        self.__auto_tune = value

    def up(self):
        """
        Tunes up.

        :return: None
        :rtype: None
        """
        self.__send('fwd')

    def down(self):
        """
        Tunes down.

        :return: None
        :rtype: None
        """
        self.__send('bwd')

    def preset_station(self, preset_number, frequency, band):
        """
        Sets a tuner preset.

        :param preset_number: The preset number.
        :type preset_number: int

        :param frequency: The station frequency.
        :type frequency: int, float

        :param band: Frequency band.
            Allowed values:
                "am"
                "fm"
        :type band: str

        :return: None
        :rtype: None
        """

        while frequency < 999999:
            frequency *= 10
        frequency = int(frequency)

        uri = 'radio:{0}?contentId={1}'.format(band, preset_number)

        self.__sony_api.send(
            'audio',
            'presetBroadcastStation',
            uri=uri,
            frequency=frequency
        )


class ParentalRatings(object):

    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, key):
        return self.__sony_api.send(
            'avContent',
            'getParentalRatingSettings'
        )[0][key]

    @property
    def parental_rating_setting_country(self):
        return self.__send('ratingCountry')

    @property
    def parental_rating_setting_unrated(self):
        return self.__send('unratedLock')

    @property
    def parental_rating_setting_age(self):
        return self.__send('ratingTypeAge')

    @property
    def parental_rating_setting_sony(self):
        return self.__send('ratingTypeSony')

    @property
    def parental_rating_setting_tv(self):
        return self.__send('ratingCustomTypeTV')

    @property
    def parental_rating_setting_mpaa(self):
        return self.__send('ratingCustomTypeMpaa')

    @property
    def parental_rating_setting_french(self):
        return self.__send('ratingCustomTypeCaFrench')

    @property
    def parental_rating_setting_english(self):
        return self.__send('ratingCustomTypeCaEnglish')
