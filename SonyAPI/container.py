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

class Container(object):
    """
    This is an arbitrary class that holds various pieces of data.

    When created from a ContainerItem instance:

    dab_info:
        dynamic_label: The dynamic label, such as song title or text
            information of advertisement.
        component_label: The component label, for a service which carries
            either audio or data.
            Example: "BBC Asian Network"
        service_label: The service label, which identifies a service in a
            textual format.
            Example: "BBC Asian Network"
        ensemble_label: The ensemble label, which identifies an ensemble in a
            textual format.
            Example: "BBC National DAB"

    state_info:
        supplement: Supplemental information about the playback status the
            device.
            Possible values:
                None - No supplemental information.
                "alarmInterrupting" - Interrupting and switching to Emergency
                    Warning System.
                "automaticMusicScanning" - Changing to next content by AMS
                    (Automatic Music Scan) function.
                "autoPresetting" - Presetting broadcast stations automatically.
                "autoScanning" - Scanning for DAB digital radio automatically.
                "bwdSeeking" - Backward seeking broadcast stations.
                "enumerating" - Enumerating storage device.
                "fwdSeeking" - Forward seeking broadcast stations.
                "initialScanning" - Initial scanning for DAB digital radio.
                "loading" - Loading a disc storage device.
                "manualSeeking" - Seeking broadcast stations manually.
                "noContent" - There is no content that can be played back.
                "noMedia" - There is no media.
                "noNextContent" - There is no next content in current playback
                    scope.
                "noPreviousContent" - There is no previous content in current
                    playback scope.
                "notAvailable" - A device can not play back for some reason.
                "presetMemorizing" - Memorizing preset of broadcast station.
                "reading" - Reading a structure of storage device.
                "receiving" - Receiving DAB digital radio. (Before initial
                    scan of DAB etc.)
                "uncontrollable" - This content can not be controlled such as
                    pause, stop, or scan by pausePlayingContent,
                    stopPlayingContent, setPlaySpeed, or
                    scanPlayingContent, and so on.
        state: Playing status.
            Possible values:
                "PLAYING" - Content is being played
                "STOPPED" - Content is stopped
                "PAUSED" - Content is pausing
                "FORWARDING" - Content is being forwarded.
    video_info:
        codec: The video codec for the content.
            Possible values:
                "" - unknown
                "avc" - MPEG4 AVC
                "mpeg1" - MPEG1 VIDEO
                "mpeg2" - MPEG2 VIDEO
                "mpeg4" - MPEG4 VIDEO
                "vc1" - VC1
                "xvid" - Xvid
                "wmv" - WMV

    audio_info:
        channel: The number of audio channels.
        frequency: The sampling audio frequency in Hz, or "" if it is
            unavailable.
            Example values:
                "44100"
                "88200"
                "96000"
        codec: The audio codec for the content.
            Possible values:
                "" - unknown
                "aac-lc"
                "f1-lpcm"
                "lpcm"

    When created from a System instance:

    forced_update: Indicates whether a forced update is required.
        Possible values:
            "true" - A forced update is required.
            "false" - A forced update is not required.
    estimated_time_sec: The estimated time required to update the application.
    updatable_version: The version the application will be after the update.
    target: The application to which this update applies.


    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            parameter_name = '_'
            for char in parameter_name:
                if char.isupper():
                    parameter_name += '_'
                parameter_name += char.lower()
            self.__dict__[parameter_name] = value

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        if '_' + item in self.__dict__:
            return self.__dict__['_' + item]

        raise AttributeError

    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        else:
            raise AttributeError
