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
import time
import datetime
from . import singleton
from .exception import UnsupportedError
from .utils import PlayTimeMixin


class HistoryItem(PlayTimeMixin):
    __metaclass__ = singleton.Singleton

    # noinspection PyPep8Naming
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

    __metaclass__ = singleton.ScheduleSingleton

    # noinspection PyPep8Naming
    def __init__(
        self,
        sony_api,
        eventId,
        uri,
        startDateTime,
        title='',
        durationSec=0,
        repeatType='',
        type="recording",
        recordingStatus='',
        quality=None,
        overlapStatus='',
        channelName=''
    ):
        if quality is None and type == "recording":
            quality = "DR"
        else:
            quality = ''

        self.__sony_api = sony_api
        self._recording_status = recordingStatus
        self._title = title
        self._quality = quality
        self._duration = durationSec
        self._uri = uri
        self._overlap_status = overlapStatus
        self._start_date_time = startDateTime
        self._repeat_type = repeatType
        self._channel_name = channelName
        self._type = type
        self._event_id = eventId

        self._supported_repeat_types = None

        self._new_settings = dict(
            type=type,
            uri=uri,
            startDateTime=startDateTime,
            durationSec=durationSec,
            eventId=eventId,
            repeatType=repeatType,
            title=title
        )

    def __send(self, method, **params):
        return self.__sony_api.send('recording', method, **params)

    @property
    def duration(self):
        """
        Gets how long to record for

        :return: a time.time instance representing the length of time
        :rtype: time.time
        """
        if self._type == 'reminder':
            self._new_settings['durationSec'] = 0

        return time.gmtime(self._new_settings['durationSec'])

    @duration.setter
    def duration(self, value):
        """
        Sets how long to record for.

        :param value: Number of seconds to record for.
        :type value: int

        :return: None
        :rtype: None
        """
        if value:
            self._type = 'recording'
        else:
            self._type = 'reminder'

        self._duration = value

    @property
    def title(self):
        """
        Gets the title of the recording.

        :return: Title of the recording
        :rtype: str
        """
        return self._new_settings['title']

    @title.setter
    def title(self, value):
        """
        Sets the title of the recording.

        :param value: New recording title if blank the device will assign a
        title.
        :type value: str

        :return: None
        :rtype: None
        """
        self._new_settings['title'] = value

    @property
    def recording_status(self):
        """
        Gets the recording status.

        :return: Possible values:
            "notStarted" - Recording this item has not started.
            "preparing" - Device is preparing for recording this item.
            "recording" - Device is now recording this item.
            "finishing" - Device is about to finish recording this item.
            "pausing" - Recording pauses for some device specific reason (and
            might restart once the reason to pause is removed.)
        :rtype: str
        """
        return self._recording_status

    @property
    def quality(self):
        """
        Gets the recording quality.

        :return: When type is "recording": "DR" - Direct recording
            When type is "reminder": ""
        :rtype: str
        """
        return self._quality

    @property
    def overlap_status(self):
        """
        Gets if the recording is overlapped with another.

        :return: Possible values:
            "notOverlapped" - No other overlap or the priority of the scheduled
            is highest.
            "fullyOverlapped" - Overlapped with others and cannot be recorded.
            "partlyOverlapped" - Overlapped with others but can be partly
            recorded.
        :rtype: str
        """
        return self._overlap_status

    @property
    def supported_repeat_types(self):
        """
        Gets the supported repeat types.

        :return: List of supported types.
            Example of supported types:
                "1" - One time.
                "d" - Every day.
                "w1" - Every Monday.
                "w2" - Every Tuesday.
                "w3" - Every Wednesday.
                "w4" - Every Thursday.
                "w5" - Every Friday.
                "w6" - Every Saturday.
                "w7" - Every Sunday.
                "w15" - Every Monday, Tuesday, Wednesday, Thursday and Friday.

            The "w##" repeat types work as follows:
                First digit is the first day, and the last digit is the last
                day of a span of days. so if you wanted Monday, Tuesday and
                Wednesday you would use W13.

        :rtype: list
        """

        if self._supported_repeat_types is None:
            self._supported_repeat_types = (
                self.__send('getSupportedRepeatType')[0]
            )

        return self._supported_repeat_types

    @property
    def repeat_type(self):
        """
        Gets the set repeat type.

        :return: See instance.supported_repeat_types
        :rtype: str
        """
        return self._new_settings['repeatType']

    @repeat_type.setter
    def repeat_type(self, value):
        """
        Sets the repeat type.

        :param value: See instance.supported_repeat_types
        :type value: str

        :return: None
        :rtype: None
        :raises: SonyAPI.UnsupportedError
        """

        if value in self.supported_repeat_types:
            self._new_settings['repeatType'] = value
        else:
            raise UnsupportedError

    @property
    def channel_name(self):
        """
        Gets the channel name.

        :return: Channel name.
        :rtype: str
        """
        return self._channel_name

    @property
    def type(self):
        """
        Gets the recording type.

        :return: Possible values:
            "recording" - scheduled item (timer reservation) for recording TV
            broadcasting program into storage.
            "reminder" - scheduled item (timer reservation) for viewing TV
            broadcasting program.
        :rtype: str
        """
        return self._new_settings['type']

    @type.setter
    def type(self, value):
        """
        Sets the recording type.

        :param value: Possible values:
            "recording" - scheduled item (timer reservation) for recording TV
            broadcasting program into storage.
            "reminder" - scheduled item (timer reservation) for viewing TV
            broadcasting program.

            if using "reminder" the duration is automatically set to 0.
            if using "recording" you will need to set the duration to the
            amount of time in seconds you want to record for
        :type value: str

        :return: None
        :rtype: None
        """

        if value == 'reminder':
            self._new_settings['durationSec'] = 0

        self._new_settings['type'] = value

    @property
    def uri(self):
        """
        Gets the location of what to record.

        :return: URI
        :rtype: str
        """
        return self._new_settings['uri']

    @uri.setter
    def uri(self, value):
        """
        Sets the location of what to record.

        :param value: URI
        :type value: str
        :return: None
        :rtype: None
        """
        self._new_settings['uri'] = value

    @property
    def event_id(self):
        """
        Gets the id of the recording.

        :return: id.
        :rtype: int
        """
        return self._event_id

    def delete(self):
        """
        Deletes this scheduled recording.

        :return: None
        :rtype: None
        """
        self.__send(
            'deleteSchedule',
            title=self._title,
            durationSec=self._duration,
            uri=self._uri,
            startDateTime=self._start_date_time,
            type=self._type,
            id=self._event_id
        )

    def save(self):
        """
        Saves this scheduled recording to the device.

        :return: None
        :rtype: None
        """
        self.delete()
        self.__send('addSchedule', **self._new_settings)

        def iter_recordings(items, idx=1):
            for item in items:
                if item['eventId'] == self._event_id:
                    self._recording_status = item['recordingStatus']
                    self._title = item['title']
                    self._quality = item['quality']
                    self._duration = item['durationSec']
                    self._uri = item['uri']
                    self._overlap_status = item['overlapStatus']
                    self._start_date_time = item['startDateTime']
                    self._repeat_type = item['repeatType']
                    self._channel_name = item['channelName']
                    self._type = item['type']

                    for key in self._new_settings.keys():
                        self._new_settings[key] = item[key]
                    break
            else:
                iter_recordings(
                    self.__send('getScheduleList', stIdx=idx * 100)[0],
                    idx + 1
                )

        iter_recordings(self.__send('getScheduleList')[0])

    @property
    def conflicts(self):
        items = self.__send('getConflictScheduleList', **self._new_settings)
        return sorted(
            list(ScheduleItem(self.__sony_api, **item) for item in items),
            key=lambda x: x.event_id
        )


class Recording(object):
    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, method, **params):
        return self.__sony_api.send('recording', method, **params)

    @property
    def scheduled(self):
        """
        Gets scheduled recordings.

        :return: a list of  SonyAPI.recording.ScheduleItem instances
        :rtype: list
        """

        items = self.__send('getScheduleList')[0]
        res = []
        i = 1
        while items:
            res += items
            items = self.__send('getScheduleList', stIdx=i * 100)[0]
            i += 1

        return sorted(
            list(ScheduleItem(self.__sony_api, **item) for item in items),
            key=lambda x: x.event_id
        )

    @property
    def status(self):
        """
        Gets the tv recording state.

        :return: Possible values:
            "notStarted" - Recording this item has not started.
            "preparing" - Device is preparing for recording this item.
            "recording" - Device is now recording this item.
            "finishing" - Device is about to finish recording this item.
            "pausing" - Recording pauses for some device specific reason (and
            might restart once the reason to pause is removed.)
        :rtype: str
        """
        return self.__send('getRecordingStatus')[0]['status']

    @property
    def failed_recordings(self):
        """
        Gets failed recordings
        :return: list of SonyAPI.recording.HistoryItem instances
        :rtype: list
        """
        items = self.__send('getHistoryList')[0]
        return list(HistoryItem(**item) for item in items)

    def new(self, uri, start_date_time, duration):
        """
        Schedules a recording.

        :param uri: What to record.
        :type uri: str
        :param start_date_time: When to record it.
        :type start_date_time: datetime.datetime or time.struct_time
        :param duration: How long to record for.
        :type duration: int or time.time

        :return: SonyAPI.recording.ScheduleItem instance
        :rtype: SonyAPI.recording.ScheduleItem
        """

        event_id = self.scheduled[-1].id + 1

        if isinstance(start_date_time, datetime.datetime):
            start_date_time = start_date_time.strftime('%Y-%m-%dT%H:%M:%S%z')
        else:
            start_date_time = time.strftime(
                '%Y-%m-%dT%H:%M:%S%z',
                time.localtime(start_date_time.tm_sec)
            )

        if isinstance(duration, time.struct_time):
            duration = duration.tm_sec

        return ScheduleItem(
            self.__sony_api,
            event_id,
            uri,
            start_date_time,
            durationSec=duration
        )
