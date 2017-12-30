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
from . import singleton
from .exception import ContentProtectedError


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

        programMediaType: Media type of broadcast program.
            TV type 1
            Example values:
                "tv" - means TV program
                "radio" - means radio program
                "data" - means data program
                "" - unknown type

        directRemoteNum: Mapped number button on remote controller.
            TV type 1
            Example values:
                int(1 through 12)

        epgVisibility: Getting the visibility on EPG application.
            TV type 2
            Example values:
                "visible" - This content is shown in EPG.
                "invisible" - This content is hidden in EPG.
                "auto" - This content is shown if this content is main channel
                    in EPG.

        channelSurfingVisibility: Getting the visibility on pushing <Channel+>
        / <Channel-> button.
            TV type 2
            Example values:
                "visible" - This content is shown.
                "invisible" - This content is hidden.

        visibility: Media type of broadcast program.
            TV type 3
            Example values:
                "visible" - This content is shown.
                "invisible" - This content is hidden.

        startDateTime: Scheduled date and time to start.
            storage
            Example values:
                ISO-8601 time format YYYY-MM-DDTHH:MM:SS.sTZD.

        channelName: Broadcaster channel name of the recorded content.
            storage
            Example values:
                "NBC", "ABC", "FOX", "HBO"

        fileSizeByte: File size of the content in bytes.
            storage
            Example values:
                int(1024)

        isAlreadyPlayed: Gets if the content been played.
            storage
            Example values:
                True - already played
                False - not played yet

        durationSec: Duration in seconds.
            storage
            Example values:
                int(300) (5 minutes)

        userContentFlag: No information
        createdTime: No information
        sizeMb: No information
        parentalCountry: No information
        parentalSystem: No information
        parentalRating: No information
        subtitleTitle: No information
        subtitleLanguage: No information
        audioChannel: No information
        audioFrequency: No information
        audioCodec: No information
        chapterCount: No information
        videoCodec: No information
        storageUri: No information
        contentType: No information
        productId: No information
        idx: No information
        status: No information

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
        self._uri = uri
        self._title = title
        self._index = index
        self._source = source
        self.__sony_api = sony_api

        self._variables = dict()

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
            return self._variables['_' + item]

        raise AttributeError

    def __setattr__(self, key, value):
        if (
            key == '_variables' or
            (
                key.startswith('_') and
                '_' + key not in self._variables
            )
        ):
            object.__setattr__(self, key, value)
        else:
            raise AttributeError

    def __send(self, method, **params):
        return self.__sony_api.send('avContent', method, **params)

    @property
    def source(self):
        return self._source

    @property
    def uri(self):
        """
        URI to identify the content item.

        :return: URI, (ex) "tv:isdbt?trip=11.22.33"
        :rtype: str
        """
        return self._uri

    @property
    def title(self):
        """
        Title of this content item.

        :return: Title, (ex) "Sports Channel"
        :rtype: str
        """
        return self._title

    @property
    def index(self):
        """
        Index of this item in the content list gotten from the source.

        :return: Source content index.
        :rtype: int
        """
        return self._index

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
        if '_is_protected' not in self._variables:
            raise AttributeError

        return self._variables['_is_protected']

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
        if '_is_protected' not in self._variables:
            raise AttributeError

        self.__dict__['_is_protected'] = value
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
        if '_is_protected' not in self._variables:
            raise AttributeError

        if self._variables['_is_protected'] is True:
            raise ContentProtectedError([
                41000,
                'This content item is protected from deletion'
            ])

        self.__send('deleteContent', uri=self.uri)

    def play(self):
        """
        Plays this content item.

        :return: None
        :rtype: None
        """
        self.__send('setPlayContent', uri=self.uri)


class SchemeItem(object):
    __metaclass__ = singleton.Singleton

    def __init__(self, sony_api, name):
        self.__sony_api = sony_api
        self._name = name.replace('_', '-')

        self.__name__ = ''
        for item in name.split('_'):
            self.__name__ += item[0].upper() + item[1:]

    def __send(self, method, **params):
        return self.__sony_api.send('avContent', method, **params)

    @property
    def name(self):
        return self._name

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

        sources = self.__send('getSourceList', scheme=self.name)
        res = []
        for source in sources:
            source = source.split(':')[1].split('?')[0]
            if source not in res:
                res += [source]

        return sorted(res)

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

    def __init__(self, scheme, sony_api, name):
        self.__sony_api = sony_api
        self._name = name.replace('_', '-')
        self._scheme = scheme
        self._uri = scheme.name + ':' + self._name

        self.__name__ = ''
        for item in name.split('_'):
            self.__name__ += item[0] + item[1:]

    @property
    def uri(self):
        return self._uri

    @property
    def name(self):
        return self._name

    @property
    def scheme(self):
        return self._scheme

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
        self._parental_ratings = None

    def __send(self, method, **params):
        return self.__sony_api.send('avContent', method, **params)

    @property
    def schemes(self):
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
        return self.__send('getSchemeList')

    @property
    def parental_ratings(self):

        if self._parental_ratings is None:
            self._parental_ratings = ParentalRatings(self.__sony__api)

        return self._parental_ratings

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if not item.startswith('_'):
            item = item.replace('_', '-')
            if item.replace('_', '-') in self.scheme_list:
                return SchemeItem(self.__sony_api, item)
        raise AttributeError

    def __getitem__(self, item):
        try:
            return getattr(self, item.replace('-', '_'))
        except AttributeError:
            raise KeyError


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
