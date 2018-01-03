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


class HistoryItem(object):
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
        self.__title = title
        self.__duration = durationSec
        self.__reason_msg = reasonMsg
        self.__reason_id = reasonId
        self.__start_date_time = startDateTime
        self.__channel_name = channelName
        self.__id = id

    @property
    def id(self):
        """
        Recording ID.

        **Getter:** Gets the recording ID.

            *Returns:* ID

            *Return type:* `int`
        """
        return self.__id

    @property
    def duration(self):
        """
        Recording length.

        **Getter:** Gets how long to record for.

            *Returns:* `time.gmtime` instance

            *Return type:* `time.gmtime`
        """

        return time.gmtime(self.__duration)

    @property
    def title(self):
        """
        Recording title.

        **Getter:** Gets the title of the recording.

            *Returns:* Recording name.

            *Return type:* `str`
        """
        return self.__title

    @property
    def reason_msg(self):
        """
        Failure reason.

        **Getter:** Gets the reason why the recoding failed..

            *Returns:* Error message.

            *Return type:* `str`
        """
        return self.__reason_msg

    @property
    def reason_id(self):
        """
        Failure id.

        **Getter:** Gets the failure id.

            *Returns:* ID.

            *Return type:* `int`
        """
        return self.__reason_id

    @property
    def start_date_time(self):
        """
        Recording start time.

        **Getter:** Gets when the recording is going to start.

            *Returns:* `datetime.datetime` instance.

            *Return type:* `datetime.datetime`
        """

        return datetime.datetime.strptime(
            self._start_date_time,
            '%Y-%m-%dT%H:%M:%S%z'
        )

    @property
    def channel_name(self):
        """
        Channel name.

        **Getter:** Gets the name of the channel.

            *Returns:* Channel name.

            *Return type:* `str`
        """
        return self.__channel_name


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
        self.__recording_status = recordingStatus
        self.__title = title
        self.__quality = quality
        self.__duration = durationSec
        self.__uri = uri
        self.__overlap_status = overlapStatus
        self.__start_date_time = startDateTime
        self.__repeat_type = repeatType
        self.__channel_name = channelName
        self.__type = type
        self.__event_id = eventId

        self.__supported_repeat_types = None

        self.__new_settings = dict(
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
        Recording length.

        **Getter:** Gets how long to record for.

            *Returns:* `time.time` instance

            *Return type:* `time.gmtime`

        **Setter:** Sets how long to record for.

            *Accepted values:*

                * `time.time` instance
                * Number of seconds

            *Value type:* `int`, 'time.time'
        """
        if self.__type == 'reminder':
            self.__new_settings['durationSec'] = 0

        return time.gmtime(self.__new_settings['durationSec'])

    @duration.setter
    def duration(self, value):
        if isinstance(value, time.struct_time):
            value = value.tm_sec

        if value:
            self.__type = 'recording'
        else:
            self.__type = 'reminder'

        self.__duration = value

    @property
    def start_date_time(self):
        """
        Recording start time.

        **Getter:** Gets when the recording is going to start.

            *Returns:* `datetime.datetime` instance.

            *Return type:* `datetime.datetime`
        """

        return datetime.datetime.strptime(
            self.__start_date_time,
            '%Y-%m-%dT%H:%M:%S%z'
        )

    @property
    def title(self):
        """
        Recording title.

        **Getter:** Gets the title of the recording.

            *Returns:* Title name.

            *Return type:* `str`

        **Setter:** Sets the title of the recording.

            *Accepted values:* Title name.

                If blank device will automatically assign a title.

            *Value type:* `str`
        """
        return self.__new_settings['title']

    @title.setter
    def title(self, value):
        self.__new_settings['title'] = value

    @property
    def recording_status(self):
        """
        Recording status.

        **Getter:** Gets the recording status.

            *Returns:*

                * ``"notStarted"`` - Recording this item has not started.
                * ``"preparing"`` - Device is preparing for recording this item.
                * ``"recording"`` - Device is now recording this item.
                * ``"finishing"`` - Device is about to finish recording this item.
                * ``"pausing"`` - Recording pauses for some device specific reason.

                    might restart once the reason to pause is removed.

            *Return type:* `str`
        """
        return self.__recording_status

    @property
    def quality(self):
        """
        Recording quality.

        **Getter:** Gets the recording quality.

            *Returns:*

                * ``"DR"`` - When type is ``"recording"``
                * ``""`` - When type is ``"reminder"``


            *Return type:* `str`
        """
        return self.__quality

    @property
    def overlap_status(self):
        """
        Recording overlapped.

        **Getter:** Gets if the recording is overlapped with another.

            *Returns:*

                * ``"notOverlapped"`` - No other overlap or the priority of the scheduled is highest.
                * ``"fullyOverlapped"`` - Overlapped with others and cannot be recorded.
                * ``"partlyOverlapped"`` - Overlapped with others but can be partly recorded.

            *Return type:* `str`
        """
        return self.__overlap_status

    @property
    def supported_repeat_types(self):
        """
        Supported repeat types

        **Getter:** Gets the supported repeat types.

            *Returns:*

                A list if supported types. Below are examples of what might
                be in the list.

                * ``"1"`` - One time.
                * ``"d"`` - Every day.
                * ``"w1"`` - Every Monday.
                * ``"w2"`` - Every Tuesday.
                * ``"w3"`` - Every Wednesday.
                * ``"w4"`` - Every Thursday.
                * ``"w5"`` - Every Friday.
                * ``"w6"`` - Every Saturday.
                * ``"w7"`` - Every Sunday.
                * ``"w15"`` - Every Monday, Tuesday, Wednesday, Thursday and Friday.

                The "w##" repeat types work as follows:
                    First digit is the first day, and the last digit is the
                    last day of a span of days. so if you wanted Monday,
                    Tuesday and Wednesday you would use W13.

            *Return type:* `list`
        """

        if self.__supported_repeat_types is None:
            self.__supported_repeat_types = (
                self.__send('getSupportedRepeatType')[0]
            )

        return self.__supported_repeat_types

    @property
    def repeat_type(self):
        """
        Repeat type

        **Getter:** Gets the set repeat type.

            *Returns:*

               Below are examples of what might be returned.

                * ``"1"`` - One time.
                * ``"d"`` - Every day.
                * ``"w1"`` - Every Monday.
                * ``"w2"`` - Every Tuesday.
                * ``"w3"`` - Every Wednesday.
                * ``"w4"`` - Every Thursday.
                * ``"w5"`` - Every Friday.
                * ``"w6"`` - Every Saturday.
                * ``"w7"`` - Every Sunday.
                * ``"w15"`` - Every Monday, Tuesday, Wednesday, Thursday and Friday.

                The "w##" repeat types work as follows:
                    First digit is the first day, and the last digit is the
                    last day of a span of days. so if you wanted Monday,
                    Tuesday and Wednesday you would use W13.

            *Return type:* `str`

        **Setter:** Sets the repeat type.

            *Possible values:*

                * ``"1"`` - One time.
                * ``"d"`` - Every day.
                * ``"w1"`` - Every Monday.
                * ``"w2"`` - Every Tuesday.
                * ``"w3"`` - Every Wednesday.
                * ``"w4"`` - Every Thursday.
                * ``"w5"`` - Every Friday.
                * ``"w6"`` - Every Saturday.
                * ``"w7"`` - Every Sunday.
                * ``"w15"`` - Every Monday, Tuesday, Wednesday, Thursday and Friday.

            *Value type:* `str`

        The "w##" repeat types work as follows:

            First digit is the first day, and the last digit is the last day
            of a span of days. so if you wanted Monday, Tuesday and Wednesday
            you would use W13.
        """
        return self.__new_settings['repeatType']

    @repeat_type.setter
    def repeat_type(self, value):
        if value in self.supported_repeat_types:
            self.__new_settings['repeatType'] = value
        else:
            raise UnsupportedError

    @property
    def channel_name(self):
        """
        Channel name.

        **Getter:** Gets the name of the channel.

            *Returns:* Channel name.

            *Return type:* `str`
        """
        return self.__channel_name

    @property
    def type(self):
        """
        Recording type.

        **Getter:** Gets the recording type.

            *Returns:*

                * ``"recording"`` - Recording TV.

                    Scheduled item (timer reservation) for recording TV
                    broadcasting program into storage.

                * ``"reminder"`` - Viewing TV.

                    Scheduled item (timer reservation) for viewing TV
                    broadcasting program.

            *Return type:* `str`

        **Setter:** Sets the recording type.

            If using "reminder" the duration is automatically set to 0.

            If using "recording" you will need to set the duration to the
            amount of time in seconds you want to record for

            *Accepted values:*

                * ``"recording"`` - Recording TV.

                    Scheduled item (timer reservation) for recording TV
                    broadcasting program into storage.

                * ``"reminder"`` - Viewing TV.

                    Scheduled item (timer reservation) for viewing TV
                    broadcasting program.

            *Value type:* `str`
        """
        return self.__new_settings['type']

    @type.setter
    def type(self, value):
        if value == 'reminder':
            self.__new_settings['durationSec'] = 0

        self.__new_settings['type'] = value

    @property
    def uri(self):
        """
        Recording URI.

        **Getter:** Gets the recording location.

            *Returns:* ``"tv:isdbt?trip=11.22.44"`` (example)

            *Return type:* `str`

        **Setter:** Sets the recording location.

            *Accepted values:* ``"tv:isdbt?trip=11.22.44"`` (example)

            *Value type:* `str`

        """
        return self.__new_settings['uri']

    @uri.setter
    def uri(self, value):
        self.__new_settings['uri'] = value

    @property
    def event_id(self):
        """
        Recording ID.

        **Getter:** Gets the id of the recording.

            *Returns:* ID

            *Return type:* `int`
        """
        return self.__event_id

    def delete(self):
        """
        Deletes this scheduled recording.
        """
        self.__send(
            'deleteSchedule',
            title=self.__title,
            durationSec=self._duration,
            uri=self.__uri,
            startDateTime=self._start_date_time,
            type=self.__type,
            id=self.__event_id
        )

    def save(self):
        """
        Saves this scheduled recording to the device.
        """
        self.delete()
        self.__send('addSchedule', **self.__new_settings)

        def iter_recordings(items, idx=1):
            for item in items:
                if item['eventId'] == self.__event_id:
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

                    for key in self.__new_settings.keys():
                        self.__new_settings[key] = item[key]
                    break
            else:
                iter_recordings(
                    self.__send('getScheduleList', stIdx=idx * 100)[0],
                    idx + 1
                )

        iter_recordings(self.__send('getScheduleList')[0])

    @property
    def conflicts(self):
        """

        Schedule conflicts

        **Getter:** ets any scheduled items that may be in conflict with this one.

            *Returns:* list of `sonyAPI.recording.ScheduleItem` instances

            *Return type:* `list`
        """
        items = self.__send('getConflictScheduleList', **self.__new_settings)
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
        Scheduled recordings.

        **Getter:** Gets a list of scheduled recordings.

            *Returns:* a list of `SonyAPI.recording.ScheduleItem` instances

            *Return type:* `list`
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
        Recording state.

        **Getter:** Gets the tv recording state.

            *Returns:*

                * ``"notStarted"`` - Recording this item has not started.
                * ``"preparing"`` - Device is preparing for recording this item.
                * ``"recording"`` - Device is now recording this item.
                * ``"finishing"`` - Device is about to finish recording this item.
                * ``"pausing"`` - Recording pauses for some device specific reason.

                    might restart once the reason to pause is removed.

            *Return type:* `str`
        """
        return self.__send('getRecordingStatus')[0]['status']

    @property
    def failed_recordings(self):
        """
        Failed recordings.

        **Getter:** Gets a list of failed recordings.

            *Returns:* a list of `SonyAPI.recording.HistoryItem` instances

            *Return type:* `list`
        """
        items = self.__send('getHistoryList')[0]
        return list(HistoryItem(**item) for item in items)

    def new(self, uri, start_date_time, duration):
        """
        Schedules a recording.

        :param uri: What to record ``"tv:isdbt?trip=11.22.44"`` (example).
        :type uri: `str`
        :param start_date_time: When to record it.
        :type start_date_time: `datetime.datetime` or `time.struct_time`
        :param duration: How long to record for.
        :type duration: `int` or `time.time`

        :return: `SonyAPI.recording.ScheduleItem` instance
        :rtype: `SonyAPI.recording.ScheduleItem`
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
