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


class InputItem(object):
    def __init__(self,  sony_api, source):
        self._sony_api = sony_api
        self._source = source

    def set(self):
        self._sony_api.send('avContent', 'setPlayContent', uri=self.uri)

    @property
    def label(self):
        status = self._status
        if not status['label']:
            return status['title']
        else:
            return status['label']

    @property
    def title(self):
        return self._status['title']

    @property
    def connection(self):
        return self._status['connection']

    @property
    def uri(self):
        return self._status['uri']

    @property
    def icon(self):
        return self._status['icon']

    @property
    def _status(self):
        results = self._sony_api.send(
            'avContent',
            'getCurrentExternalInputsStatus'
        )

        for result in results:
            if result.uri == self._source:
                return result
