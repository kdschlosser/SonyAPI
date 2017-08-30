# -*- coding: utf-8 -*-
#
# SonyAPI
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


from utils import get_icon
import requests


class Application(object):
    def __init__(self, sony_api, title='', uri='', data='', icon=''):
        self._sony_api = sony_api
        self.title = title
        self.data = data
        self.uri = uri
        if (
            icon and
            sony_api._ip_address.split(':')[0] not in icon and
            icon not in sony_api.icon_cache
        ):
            self.display_icon = get_icon(icon)
            sony_api.icon_cache[icon] = self.display_icon
        else:
            self.display_icon = None
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
