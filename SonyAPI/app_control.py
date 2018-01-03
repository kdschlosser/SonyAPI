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
from .utils import get_icon
from . import singleton, encryption
import requests

class AppControl(object):
    def __init__(self, sony_api):

        self.__sony_api = sony_api
        self._cipher = encryption.Encryption(sony_api)

    def __send(self, method, **params):
        return self.__sony_api.send('appControl', method, **params)

    @property
    def application_status_list(self):
        """
        Gets active application status.

        :return: list of (status type, state)
            Status Types:
                "textInput" - software keyboard
                "cursorDisplay" - application using cursor
                "webBrowse" - web browser
            States:
                True - "on", application is active
                False - "off", application is inactive
        :rtype: list
        """
        statuses = self.__send('getApplicationStatusList')
        return list(
            (status['name'], True if status['status'] == 'on' else False)
            for status in statuses
        )

    @property
    def application_list(self):
        """
        Gets the list of applications that can be launched.

        :return: list of SonyAPI.app_control.ApplicationItem instances
        :rtype: list
        """
        applications = self.__send('getApplicationList')
        return list(
            ApplicationItem(self.__sony_api, **app) for app in applications
        )

    def terminate_applications(self):
        """
        Terminates all running applications.

        :return: None
        :rtype: None
        """
        self.__send('terminateApps')

    def application_csx_account(self, user_id, user_name, token):
        """
        Sets account information to log-in CSX services.

        This will help end users to avoid annoying account setting both on
        client and server device.

        :param user_id: User id.
        :type user_id: str
        :param user_name: Username to display.
        :type user_name: str
        :param token: Access token.
        :type token: str
        :return: None
        :rtype: None
        """

        self.__send(
            'setCsxUserAccount',
            encKey=self._cipher.key,
            userName=user_name,
            accessToken=self._cipher.encrypt(token),
            userID=user_id
        )

    @property
    def text_form(self):
        """
        Gets text form.

        :return: text form
        :rtype: text
        """
        text = self.__send('getTextForm', encKey=self._cipher.key)[0]['text']
        return self._cipher.decrypt(text)

    @text_form.setter
    def text_form(self, value):
        """
        Sets text form.

        :param value: Text to be sent.
        :type value: str
        :return: None
        """
        self.__send(
            'setTextForm',
            encKey=self._cipher.key,
            text=self._cipher.encrypt(value)
        )


class ApplicationItem(object):

    __metaclass__ = singleton.Singleton

    def __init__(self, sony_api, title='', uri='', data='', icon=''):
        self.__sony_api = sony_api
        self._title = title
        self._data = data
        self._uri = uri
        self._display_icon = None
        self._icon = icon

    @property
    def icon(self):
        return self._icon

    @property
    def title(self):
        return self._title

    @property
    def data(self):
        return self._data

    @property
    def uri(self):
        return self._uri

    @property
    def display_icon(self):
        if self._display_icon is None:
            if self.__sony_api.cache_icons and self.icon:
                ip = self.__sony_api.url.split('/')[2]

                if self.icon in self.__sony_api.icon_cache:
                    self._display_icon = self.__sony_api.icon_cache[self.icon]
                elif ip.split(':')[0] not in self.icon:
                    self._display_icon = get_icon(self.icon)
                    self.__sony_api.icon_cache[self.icon] = self._display_icon
        return self._display_icon

    def start(self):
        self.__sender(requests.post, '')

    def stop(self):
        self.__sender(requests.delete, '/run')

    def status(self):
        return self.__sender(requests.get, '')

    def __send(self, method, **params):
        return self.__sony_api.send('appControl', method, **params)

    def __sender(self, func, url):
        ip = self.__sony_api.url.split('/')[2]

        headers = {
            'Origin': 'package:com.google.android.youtube',
            'Host': ip
        }

        response = func(
            'http://' + ip + '/DIAL/apps/' + self.title + url,
            **headers
        )
        return response.read()

    def active(self):
        """
        Sets this Application as the active one.

        :return: None
        :rtype: None
        """
        self.__sony_api.send('setActiveApp', uri=self.uri)
