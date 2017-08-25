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


class BrowserItem(object):
    def __init__(self, sony_api, title, url, data='', icon=''):
        self._sony_api = sony_api
        self.title = title
        self.data = data
        self.url = url
        if icon:
            self.display_icon = get_icon(icon)
        else:
            self.display_icon = None
        self.icon = icon

    def load(self):
        self._sony_api.send('browser', 'setTextUrl', url=self.url)


class UrlItem(BrowserItem):
    pass


class BookmarkItem(BrowserItem):
    pass
