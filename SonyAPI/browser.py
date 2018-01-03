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
from . import singleton
from .utils import create_icon
from base64 import b64decode, b64encode


class BrowserItem(object):
    __metaclass__ = singleton.BrowserSingleton

    def __init__(self, sony_api, url='', title='', type='', favicon=''):
        self.__sony_api = sony_api
        self.title = title
        self.fav_icon_type = type
        self.url = url
        if favicon:
            self.display_icon = create_icon(b64decode(favicon))
        else:
            self.display_icon = None
        self.fav_icon = favicon

    def load(self):
        """
        Loads this website.

        :return: None
        :rtype: None
        """
        self.__sony_api.send(
            'browser',
            'setTextUrl',
            url=self.url,
            title=self.title,
            favicon=self.fav_icon,
            type=self.fav_icon_type
        )

    def icon(self, (icon_data, icon_type)):
        """
        Sets the icon for this page.

        :param icon_data: Icon data
        :type icon_data: str
        :param icon_type: Icon type - png, jpg, gif....
        :type icon_type: str
        :return: None
        :rtype: None
        """
        self.fav_icon = b64encode(icon_data)
        self.fav_icon_type = icon_type

    icon = property(fset=icon)


class UrlItem(BrowserItem):
    pass


class BookmarkItem(BrowserItem):
    pass


class Browser(object):

    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, method, **params):
        return self.__sony_api.send('browser', method, *params)

    @property
    def bookmark_list(self):
        """
        Gets the bookmarks in the browser.

        :return: list of SonyAPI.Browser.BookmarkItem instances
        :rtype: list
        """

        return list(
            BookmarkItem(self.__sony_api, **item)
            for item in self.__send('getBrowserBookmarkList')[0]
        )

    def back(self):
        """
        Moves browser back one page.

        :return: None
        :rtype: None
        """
        self.__send('actBrowserControl', control="back")

    def forward(self):
        """
        Moves browser forward one page.

        :return: None
        :rtype: None
        """
        self.__send('actBrowserControl', control="forward")

    def reload(self):
        """
        Reloads the current browser page.

        :return: None
        :rtype: None
        """
        self.__send('actBrowserControl', control="reload")

    def stop(self):
        """
        Stops the browser.

        :return: None
        :rtype: None
        """
        self.__send('actBrowserControl', control="stop")

    def zoom_in(self):
        """
        Zoom in the current browser page.

        :return: None
        :rtype: None
        """
        self.__send('actBrowserControl', control="zoomIn")

    def zoom_out(self):
        """
        Zoom out the current browser page.

        :return: None
        :rtype: None
        """
        self.__send('actBrowserControl', control="zoomOut")

    @property
    def url(self):
        """
        Gets the current active browser page.

        :return: SonyAPI.Browser.UrlItem instance
        :rtype: SonyAPI.Browser.UrlItem
        """
        url = self.__send('getTextUrl')[0]
        return UrlItem(self.__sony_api, **url)

    def new_page(self, url):
        """
        Creates a new SonyAPI.Browser.UrlItem instance.

        With this new instance you are able to set the title as well as an
        icon. You can also load the page from that instance.

        instance.title = 'Some Title'
        instance.icon = (str(icon data), 'png')
        instance.load()

        :param url: URL of the web page.
        :type url: str
        :return: SonyAPI.Browser.UrlItem instance
        :rtype: SonyAPI.Browser.UrlItem instance
        """
        return UrlItem(self.__sony_api, url=url)
