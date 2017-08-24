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


class InputItem(object):
    def __init__(self,  sony_api, connection, label, uri, icon, title):
        self._sony_api = sony_api
        self.title = title
        self.connection = connection
        self.uri = uri
        self.label = label
        if icon:
            self.display_icon = get_icon(icon)
        else:
            self.display_icon = None
        self.icon = icon

    def set(self):
        self._sony_api.send('sony/avContent', 'setPlayContent', uri=self.uri)
