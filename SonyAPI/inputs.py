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
from . import media


class InputItem(object):
    def __init__(self,  sony_api, source):
        self._sony_api = sony_api
        self._source = source

        status = self._status

        if not status['label']:
            self.label = status['title']
        else:
            self.label = status['label']

        self.title = status['title']
        self.uri = status['uri']
        self.icon = status['icon']

    def set(self):
        self._sony_api.send('avContent', 'setPlayContent', uri=self.uri)

    @property
    def content(self):
        content_list = self._sony_api.send(
            'avContent',
            'getContentList',
            source=self.uri
        )
        content_items = []
        for content in content_list:
            content['source'] = self
            content_items += [media.ContentItem(self, **content)]
        return content_items

    @property
    def connection(self):
        return self._status['connection']

    @property
    def _status(self):
        results = self._sony_api.send(
            'avContent',
            'getCurrentExternalInputsStatus'
        )

        for result in results:
            if result['uri'] == self._source:
                return result
