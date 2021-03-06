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
from .utils import PlayTimeMixin


class HistoryItem(PlayTimeMixin):
    def __init__(
        self,
        title,
        durationSec,
        reasonMsg,
        reasonId,
        startDateTime,
        channelName,
        id
    ):
        self.title = title
        self._duration = durationSec
        self.reason_msg = reasonMsg
        self.reason_id = reasonId
        self._start_date_time = startDateTime
        self.channel_name = channelName
        self.id = id


class ScheduleItem(PlayTimeMixin):

    def __init__(
        self,
        sony_api,
        recordingStatus,
        title,
        quality,
        durationSec,
        uri,
        overlapStatus,
        startDateTime,
        repeatType,
        channelName,
        type,
        id
    ):
        self._sony_api = sony_api
        self.recording_status = recordingStatus
        self.title = title
        self.quality = quality
        self._duration = durationSec
        self.uri = uri
        self.overlap_status = overlapStatus
        self._start_date_time = startDateTime
        self.repeat_type = repeatType
        self.channel_name = channelName
        self.type = type
        self.id = id

    def delete(self):
        self._sony_api.send(
            'recording',
            'deleteSchedule',
            title=self.title,
            durationSec=self._duration,
            uri=self.uri,
            startDateTime=self._start_date_time,
            type=self.type,
            id=self.id
        )

