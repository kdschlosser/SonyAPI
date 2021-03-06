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

import re
import time
import requests
import threading
from .logger import LOGGER as _LOGGER
from subprocess import Popen, PIPE
from datetime import datetime

try:
    StringIO = __import__('cStringIO.StringIO')
except ImportError:
    from io import StringIO

DATE = '%Y-%m-%dT%H:%M:%S'


def get_mac_addresses(ip_addresses):
    for ip_address in ip_addresses:
        Popen(["ping", "-c 1", ip_address], stdout=PIPE)
    proc = Popen("arp -a", stdout=PIPE)
    data = proc.communicate()[0]

    results = []

    for ip_address in ip_addresses[:]:
        if ip_address in data:
            ip_data = data[data.find(ip_address):]
            mac = re.search(r"(([a-f\d]{1,2}:){5}[a-f\d]{1,2})", ip_data)
            if mac is None:
                mac = re.search(r"(([a-f\d]{1,2}-){5}[a-f\d]{1,2})", ip_data)
            if mac is not None:
                mac = mac.groups()[0].replace('-', ':').upper()
            else:
                mac = '00:00:00:00:00:00'
            results += [[ip_address, mac]]
            ip_addresses.remove(ip_address)
            _LOGGER.debug(
                '||',
                results=results,
                ip_address=ip_address,
                mac=mac
            )

    return results


def cache_icons(sony_api, event):
    applications = sony_api.send('appControl', 'getApplicationList')

    lock1 = threading.Lock()
    lock2 = threading.Lock()

    def get_icons():

        while applications and not event.isSet():
            lock1.acquire()
            app = applications.pop(0)
            lock1.release()
            icon = app['icon']
            if (
                icon and
                sony_api._ip_address.split(':')[0] not in icon and
                icon not in sony_api.icon_cache
            ):
                try:
                    tmp_icon = get_icon(icon)
                    lock2.acquire()
                    sony_api.icon_cache[icon] = tmp_icon
                    lock2.release()
                except:
                    pass

    threads = []
    for i in range(4):
        threads += [threading.Thread(target=get_icons)]
        threads[-1].start()

    while applications and not event.isSet():
        pass

    if event.isSet():
        for thread in threads:
            if thread.isAlive():
                thread.join(3.0)


def get_icon(url):
    icon_data = requests.get(url).content
    icon = StringIO()
    try:
        icon.write(icon_data)
    except:
        pass
    icon.seek(0)
    return icon


class PlayTimeMixin(object):
    _duration = 0
    _start_date_time = ''

    @property
    def duration(self):
        return time.gmtime(self._duration)

    @property
    def start_time(self):
        start_time = self._start_date_time
        if start_time:
            try:
                start_time = (
                    datetime.time(datetime.strptime(start_time[:-5], DATE))
                )
            except TypeError:
                start_time = datetime.time(
                    datetime(*(time.strptime(start_time[:-5], DATE)[0:6]))
                )

            return start_time

    @property
    def remaining(self):
        elapsed = self.elapsed
        if elapsed is not None:
            return self.duration - elapsed

    @property
    def elapsed(self):
        start_time = self._start_date_time
        if start_time:
            try:
                elapsed = datetime.now() - datetime.strptime(
                    start_time[:-5],
                    DATE
                )
            except TypeError:
                elapsed = (
                    datetime.now() -
                    datetime(*(time.strptime(start_time[:-5], DATE)[0:6]))
                )
            return elapsed

    @property
    def percent_elapsed(self):
        elapsed = self.elapsed
        if elapsed is not None:
            rounded_elapsed = (
                round(((elapsed.seconds / self.duration.seconds) * 100), 0)
            )
            percent_elapsed = int(rounded_elapsed)

            return percent_elapsed

    @property
    def end_time(self):
        start_time = self.start_time
        if start_time is not None:
            return start_time + self.duration
