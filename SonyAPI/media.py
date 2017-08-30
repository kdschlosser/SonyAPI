# -*- coding: utf-8 -*-
#
#  SonyAPI
# Copyright (C) 2017 Kevin Schlosser

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from utils import PlayTimeMixin


class ContentBase(PlayTimeMixin):
    source = ''
    _sony_api = None
    uri = ''
    title = ''

    def tv_content_visibility(
        self,
        visibility='',
        surfing_visibility='',
        epg_visibility=''
    ):
        if self.source.startswith('tv'):
            self._sony_api.send(
                'avContent',
                'setTvContentVisibility',
                channelSurfingVisibility=surfing_visibility,
                uri=self.uri,
                visibility=visibility,
                epgVisibility=epg_visibility
            )
        else:
            raise NotImplementedError

    def delete_protection(self, enable):
        self._sony_api.send(
            'avContent',
            'setDeleteProtection',
            isProtected=enable,
            uri=self.uri
        )

    property(fset=delete_protection)

    def add_recording_schedule(self, quality='', repeat_type=''):
        self._sony_api.send(
            'recording',
            'addSchedule',
            title=self.title,
            quality=quality,
            durationSec=self._duration,
            uri=self.uri,
            startDateTime=self._start_date_time,
            repeatType=repeat_type,
        )

        for item in self._sony_api.recording_schedule_list:
            if (
                self.title == item.title and
                self.uri == item.uri and
                str(self.start_time) == str(item.start_time)
            ):
                return item

    def remove_recording_schedule(self):
        for item in self._sony_api.recording_schedule_list:
            if (
                self.title == item.title and
                self.uri == item.uri and
                str(self.start_time) == str(item.start_time)
            ):
                item.delete()


class ContentItem(ContentBase):

    def __init__(
        self,
        sony_api,
        index=0,
        tripletStr='',
        title='',
        directRemoteNum='',
        isProtected=False,
        isAlreadyPlayed=False,
        durationSec=0,
        uri='',
        programNum='',
        dispNum='',
        originalDispNum='',
        startDateTime='',
        programMediaType='',
        channelName='',
        source='',
        userContentFlag='',
        createdTime='',
        sizeMb='',
        parentalCountry='',
        parentalSystem='',
        parentalRating='',
        subtitleTitle='',
        subtitleLanguage='',
        audioChannel='',
        audioFrequency='',
        audioCodec='',
        chapterCount='',
        videoCodec='',
        storageUri='',
        contentType='',
        productId='',
        fileSizeByte='',
        visibility='',
        channelSurfingVisibility='',
        epgVisibility='',
        idx='',
        status=''
    ):
        self._sony_api = sony_api
        self.index = index
        self.triplet_str = tripletStr
        self.title = title
        self.direct_remote_num = directRemoteNum
        self.is_protected = isProtected
        self.is_already_played = isAlreadyPlayed
        self._duration = durationSec
        self.uri = uri
        self.program_num = programNum
        self.display_num = dispNum
        self.original_display_num = originalDispNum
        self._start_date_time = startDateTime
        self.program_media_type = programMediaType
        self.channel_name = channelName
        self.source = source
        self.user_content_flag = userContentFlag
        self.created_time = createdTime
        self.size_mb = sizeMb
        self.parental_country = parentalCountry
        self.parental_system = parentalSystem
        self.parental_rating = parentalRating
        self.subtitle_title = subtitleTitle
        self.subtitle_language = subtitleLanguage
        self.audio_channel = audioChannel
        self.audio_frequency = audioFrequency
        self.audio_codec = audioCodec
        self.chapter_count = chapterCount
        self.video_codec = videoCodec
        self.storage_uri = storageUri
        self.content_type = contentType
        self.product_id = productId
        self.file_size_byte = fileSizeByte
        self.visibility = visibility
        self.channel_surfing_visibility = channelSurfingVisibility
        self.epg_visibility = epgVisibility
        self.idx = idx
        self.status = status

    def set(self):
        if 'tv' in self.uri:
            self._sony_api.send(
                'avContent',
                'setPlayTvContent',
                channel=str(self.display_num)
            )
        else:
            self._sony_api.send('avContent', 'setPlayContent', uri=self.uri)

    def delete(self):
        self._sony_api.send('avContent', 'deleteContent', uri=self.uri)


class NowPlaying(ContentBase):

    def __init__(
        self,
        sony_api,
        programTitle='',
        tripletStr='',
        title='',
        bivl_provider='',
        durationSec=0,
        uri='',
        programNum='',
        mediaType='',
        source='',
        dispNum='',
        originalDispNum='',
        startDateTime='',
        bivl_assetId='',
        bivl_serviceId='',
        playSpeed=''
    ):
        self._sony_api = sony_api
        self.program_title = programTitle
        self.triplet_str = tripletStr
        self.title = title
        self.bivl_provider = bivl_provider
        self._duration = durationSec
        self.uri = uri
        self.program_num = programNum
        self.media_type = mediaType
        self.display_num = dispNum
        self.original_display_num = originalDispNum
        self._start_date_time = startDateTime
        self.bivl_asset_id = bivl_assetId
        self.bivl_service_id = bivl_serviceId
        self.play_speed = playSpeed

        self.source = source
        for s in sony_api.source_list:
            if s.uri == source or s.uri == uri:
                self.source = s
                break

# {
# u'programTitle': u'program title',
#  u'tripletStr': u'8835.11.2010',
#  u'title': u'some title',
#  u'durationSec': 6300,
#  u'uri': u'tv:dvbt?trip=8835.11.2010&srvName=11%20%D0%A0%D0%95%D0%9D%20%D0%A2%D0%92',
# u'source': u'tv:dvbt',
#  u'dispNum': u'011',
# u'startDateTime': u'2014-10-16T01:45:00+0400',
#  u'programMediaType': u'tv'
# }
