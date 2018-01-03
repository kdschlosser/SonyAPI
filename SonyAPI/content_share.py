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
import requests

from . import singleton
from .utils import get_icon


class ContentShare(object):

    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, method, **params):
        return self.__sony_api.send('contentshare', method, **params)

    def close(self):
        """
        Closes content share.

        :return: None
        :rtype: None
        """

        self.__send('closeContentShare')

    @property
    def photos(self):
        """
        Gets photos.

        :return: list of SonyAPI.content_share.ContentItem instances
        :rtype: list
        """

        items = self.__send('getContentList', type='photos')
        i = 50
        photos = []
        while items:
            photos += items
            items = self.__send('getContentList', type='photos', index=i)
            i += 50
        return list(PhotoItem(self.__sony_api, **item) for item in items)

    @property
    def videos(self):
        """
        Gets videos.

        :return: list of SonyAPI.content_share.ContentItem instances
        :rtype: list
        """

        items = self.__send('getContentList', type='videos')
        i = 50
        photos = []
        while items:
            photos += items
            items = self.__send('getContentList', type='videos', index=i)
            i += 50
        return list(ContentItem(self.__sony_api, **item) for item in items)

    @property
    def music(self):
        """
        Gets music.

        :return: list of SonyAPI.content_share.ContentItem instances
        :rtype: list
        """

        items = self.__send('getContentList', type='music')
        i = 50
        photos = []
        while items:
            photos += items
            items = self.__send('getContentList', type='music', index=i)
            i += 50
        return list(ContentItem(self.__sony_api, **item) for item in items)

    @property
    def server(self):
        """
        Gets server connection information.

        :return: Dictionary containing connection info.
            ssid - SSID. If a server is set as WiFi Direct access point, this
                value is returned.
            keyType - Wireless encryption type.
            key - Key code to access wireless access point.
            deviceName - Friendly name of the server device that can be
                configured by end user
            url - ContentShare application URL.
            touchPadRemote - Server's capability to handle touchpad remote
                controller.
                "notSupported" - Touchpad remote is not supported.
                "active" - Touchpad remote is registered to server.
                "inactive" - Touchpad remote is not registered to server.
        :rtype: dict
        """

        return self.__send('getContentShareServerInfo')

    @property
    def users(self):
        """
        Gets user list.

        :return: list of users.
        :rtype: list
        """

        users = self.__send('getUserList')[0]

        return list(UserItem(self.__sony_api, **user) for user in users)

    def bgm_control_mode(self, (value, url)):
        """
        Sets if BGM is played or not.

        :param value: Possible values:
            True - BGM is played.
            False - BGM is not played.
        :type value: bool

        :param url: URL of BGM content.
        :type url: str
        :return: None
        :rtype: None
        """
        self.__send('setBgmControlMode', playback=value, url=url)

    def quick_invitation_mode(self, value):
        """
        Request PhotoShare application to show/hide quick invitation
        information which is necessary for client to connect with PhotoShare
        server.

        :param value: Possible values:
            "shown" - Quick invitation screen is shown.
            "hidden" - Quick invitation screen is hidden.

        :return: None
        :rtype: None
        """
        self.__send('setQuickInvitationMode', mode=value)

    def user_nickname(self, (nickname, uuid)):
        """
        Set/Update client's nickname related to uuid.

        Nickname is expected to be displayed to identify each user who joins.

        :param nickname: Nickname of a client that can be configured by user
            to display.
        :type nickname: str
        :param uuid: Unique ID of a client.
        :type uuid: str

        :return: None
        :rtype: None
        """
        self.__send('setUserNickName', nickname=nickname, uuid=uuid)

    bgm_control_mode = property(fset=bgm_control_mode)
    quick_invitation_mode = property(fset=quick_invitation_mode)
    user_nickname = property(fset=user_nickname)


class UserItem(object):
    __metaclass__ = singleton.Singleton

    # noinspection PyPep8Naming
    def __init__(
        self,
        sony_api,
        uuid,
        userNickname,
        avatarUri
    ):
        self._uuid = uuid
        self._nickname = userNickname
        self._avatar_uri = avatarUri
        self._avatar = None
        self.__sony_api = sony_api

    def __send(self, method, **params):
        return self.__sony_api.send('contentshare', method, **params)

    @property
    def uuid(self):
        return self._uuid

    @property
    def nickname(self):
        return self._nickname

    @property
    def avatar_uri(self):
        return self._avatar_uri

    @property
    def avatar(self):
        if self._avatar is None and self._avatar_uri:
            self._avatar = get_icon(self._avatar_uri)
        return self._avatar


class ContentItem(object):
    """
    Attributes:
        index: Index of the list, starting with "index" indicated in the
            request.
        file_name: Filename of the content. (unique key used in playContent)
        file_name_alias: Alias of filename of the content. (unique key used in
            playContent)
        uuid: Client uuid.
        user_nickname: Nickname of a client that can be configured by user to
            display
        original_url: URL of the original content uploaded by client.
        thumbnail_url: URL of the content converted by server for thumbnail
            use.
        original_orientation: Orientation of the original content uploaded by
            client. Value definition is same as exif orientation attribute.
        thumbnail_orientation: Orientation of the content converted by server
            for thumbnail use.Value definition is same as exif orientation
            attribute.
        artist_name: Artist name of the content.
        status: Playing status of the content.
            "stopped" - stopped
            "playing" - playing.
            "paused" - paused

        type: content type
            "photo" - photo.
            "video" - video
            "music" - music

        voted_list_by_uuid: List of uuid who has voted on this content.
        size: Content size (byte).
    """

    __metaclass__ = singleton.Singleton

    # noinspection PyPep8Naming
    def __init__(
        self,
        sony_api,
        index,
        fileName,
        fileNameAlias,
        uuid,
        userNickname,
        originalUrl,
        thumbnailUrl,
        originalOrientation,
        thumbnailOrientation,
        artistName,
        status,
        type,
        votedListByUuid,
        size
    ):
        self.index = index
        self.file_name = fileName
        self.file_name_alias = fileNameAlias
        self.uuid = uuid
        self.user_nickname = userNickname
        self.original_url = originalUrl
        self.thumbnail_url = thumbnailUrl
        self.original_orientation = originalOrientation
        self.thumbnail_orientation = thumbnailOrientation
        self.artist_name = artistName
        self.status = status
        self.type = type
        self.voted_list_by_uuid = votedListByUuid
        self.size = size
        self.__sony_api = sony_api
        self._thumbnail = None
        self._original = None

    def __send(self, method, **params):
        return self.__sony_api.send('contentshare', method, **params)

    @property
    def thumbnail(self):
        if self._thumbnail is None:
            if self.thumbnail_url:
                self._thumbnail = get_icon(self.thumbnail_url)
        return self._thumbnail

    @property
    def original(self):
        if self._original is None:
            if self.original_url:
                if self.type == "photo":
                    self._original = get_icon(self.original_url)
                else:
                    self._original = requests.get(self.original_url).content
        return self._original

    def toggle_play(self):
        self.__send('togglePlayStatus', fileName=self.file_name)

    def vote(self, client_uuid):
        self.__send('voteContent', fileName=self.file_name, uuid=client_uuid)


class PhotoItem(ContentItem):

    def rotate_photo(self, degrees):
        self.__send(
            'rotatePhoto',
            rotationDegree=degrees,
            fileName=self.file_name
        )
