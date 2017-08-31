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
import requests


class Application(object):
    def __init__(self, sony_api, title='', uri='', data='', icon=''):
        self._sony_api = sony_api
        self.title = title
        self.data = data
        self.uri = uri
        self.display_icon = None

        if icon and icon not in sony_api.icon_cache:
            if sony_api._ip_address.split(':')[0] not in icon:
                self.display_icon = get_icon(icon)
                sony_api.icon_cache[icon] = self.display_icon

        self.icon = icon

    def start(self):
        self._send(requests.post, '')

    def stop(self):
        self._send(requests.delete, '/run')

    def status(self):
        return self._send(requests.get, '')

    def _send(self, func, url):
        ip = self._sony_api._ip_address
        headers = {
            'Origin': 'package:com.google.android.youtube',
            'Host':   ip
        }

        response = func(
            'http://' + ip + ':80/DIAL/apps/' + self.title + url,
            **headers
        )
        return response.read()

    def active(self):
        self._sony_api.send('appControl', 'setActiveApp', uri=self.uri)
