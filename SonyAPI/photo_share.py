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
from .utils import get_icon
from . import singleton


class PhotoShare(object):

    def __init__(self, sony_api):
        self._sony_api = sony_api

    def __send(self, method, **params):
        return self._sony_api('photoshare', method, **params)[0]

    def close(self):
        """
        Terminate PhotoShare application.

        :return: None
        :rtype: None
        """

        self.__send('closePhotoShare')

    @property
    def photos(self):
        """
        Gets the list of photos uploaded to server.

        :return: List of SonyApi.photoshare.Photo instances
        :rtype: list
        """

        photos = self.__send('getPhotoList')
        res = []
        i = 50
        while photos:
            res += photos
            photos = self.__send('getPhotoList', index=i)[0]
            i += 50
        return list(Photo(self._sony_api, **photo) for photo in photos)

    @property
    def server(self):
        """
        Gets information needed to access to PhotoShare application.

        The user with already connected client can show this information to
        another user who want to join PhotoShare.

        :return: Connection information:
            Example:
                "keyType" - "WPA2",
                "deviceName" - "BRAVIA",
                "ssid" - "DIRECT-XX-BRAVIA",
                "touchPadRemote" - "active",
                "url" -  "http://192.168.172.1/p",
                "key" - "abcd1234"

        :rtype: dict
        """
        return self.__send('getPhotoShareServerInfo')[0]

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


class Photo(object):
    """
    Properties:
        index: Index of the list, starting with "index" indicated in the
            request.
        file_name : Filename of the photo. (unique key used in
            playPhotoContent)
        uuid: Client uuid.
        user_nickname: Nickname of a client that can be configured by user to
            display
        original_url: URL of the original photo uploaded by client.
        thumbnail_url: URL of the photo converted by server for thumbnail use.
        original_orientation: Orientation of the original photo uploaded by
            client. Value definition is same as exif orientation attribute.
        thumbnail_orientation: Orientation of the photo converted by server for
            thumbnail use.Value definition is same as exif orientation
            attribute.
        thumbnail: StringIO file like object of the thumbnail.
        photo: StringIO file like object of the photo.
    """

    __metaclass__ = singleton.Singleton

    # noinspection PyPep8Naming
    def __init__(
        self,
        sony_api,
        index,
        fileName,
        uuid,
        userNickname,
        originalUrl,
        thumbnailUrl,
        originalOrientation,
        thumbnailOrientation
    ):
        self._sony_api = sony_api

        self._index = index
        self._file_name = fileName
        self._uuid = uuid
        self._user_nickname = userNickname
        self._original_url = originalUrl
        self._thumbnail_url = thumbnailUrl
        self._original_orientation = originalOrientation
        self._thumbnail_orientation = thumbnailOrientation
        self._photo = None
        self._thumbnail = None

    @property
    def index(self):
        return self._index

    @property
    def file_name(self):
        return self._file_name

    @property
    def uuid(self):
        return self._uuid

    @property
    def user_nickname(self):
        return self._user_nickname

    @property
    def original_url(self):
        return self._original_url

    @property
    def thumbnail_url(self):
        return self._thumbnail_url

    @property
    def original_orientation(self):
        return self._original_orientation

    @property
    def thumbnail_orientation(self):
        return self._thumbnail_orientation

    @property
    def photo(self):
        if self._photo is None and self._original_url:
            self._photo = get_icon(self._original_url)
        return self._photo

    @property
    def thumbnail(self):
        if self._thumbnail is None and self._thumbnail_url:
            self._thumbnail = get_icon(self._thumbnail_url)
        return self._thumbnail

    def __send(self, method, **params):
        return self._sony_api('photoshare', method, **params)[0]

    def play(self):
        self.__send('playPhotoContent', fileName=self.file_name)
