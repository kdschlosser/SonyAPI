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


import requests
import socket
import threading
from api_const import (
    VOLUME_EVENT,
    MUTE_EVENT,
    SOURCE_EVENT,
    CHANNEL_EVENT,
    POWER_EVENT,
    MEDIA_EVENT,
)


class Base(object):
    service = ''
    local_port = None

    def __init__(self, ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        self.local_ip_address = s.getsockname()[0]
        self.url = 'http://%s:52323/upnp/event/%s' % (ip, self.service)
        self.header = dict(
            NT='upnp:event',
            CALLBACK=(
                '<http://%s:%d/>' % (self.local_ip_address, self.local_port)
            ),
            TIMEOUT='Second-1800'
        )
        self.sid = None
        self.sock = None
        self._callbacks = []
        self._listen_event = threading.Event()
        self._listen_thread = threading.Thread(target=self.listen)

    def add_callback(self, callback):
        if callback not in self._callbacks:
            self._callbacks += [callback]

    def remove_callback(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def callback_count(self):
        return len(self._callbacks)

    def listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1700)
        self.sock.bind((self.local_ip_address, self.local_port))

        while not self._listen_event.isSet():
            try:
                self.sock.listen(3)
                conn, address = self.sock.accept()
                data = conn.recv(4096)
                conn.close()
                print(data)
            except socket.timeout:
                header = dict(
                    SID=self.sid,
                    TIMEOUT='Second-1800'
                )
                requests.request(
                    'SUBSCRIBE',
                    self.url,
                    headers=header
                )

        header = dict(
            SID=self.sid
        )
        requests.request('UNSUBSCRIBE', self.url, headers=header)

    def start(self):
        response = requests.request(
            'SUBSCRIBE',
            self.url,
            headers=self.header
        )
        self.sid = response.headers['SID']
        self._listen_thread.start()

    def stop(self):
        self._listen_event.set()
        self.sock.shutdown(socket.SHUT_RDWR)
        self._listen_thread.join(3.0)


class RenderingControl(Base):
    service = 'RenderingControl'
    local_port = 8000


class AVTransport(Base):
    service = 'AvTransport'
    local_port = 8001


class ConnectionManager(Base):
    service = 'ConnectionManager'
    local_port = 8002


class IRCC(Base):
    service = 'IRCC'
    local_port = 8003
