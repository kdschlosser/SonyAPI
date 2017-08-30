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


try:
    PY2 = bool(unicode)
except NameError:
    PY2 = False

GUID = '24F26C67-5A50-4B08-8754-80EBAF880379'

VOLUME_EVENT = 0x1
MUTE_EVENT = 0x2
SOURCE_EVENT = 0x3
CHANNEL_EVENT = 0x4
POWER_EVENT = 0x5
MEDIA_EVENT = 0x6

SSDP_ADDR = "239.255.255.250"
SSDP_PORT = 1900
SSDP_MX = 1
SSDP_ST = "urn:schemas-sony-com:service:ScalarWebAPI:1"

SSDP_REQUEST = (
    'M-SEARCH * HTTP/1.1\r\n'
    'HOST: %s:%d\r\n'
    'MAN: "ssdp:discover"\r\n'
    'MX: %d\r\n'
    'ST: %s\r\n'
    '\r\n' % (SSDP_ADDR, SSDP_PORT, SSDP_MX, SSDP_ST)
)

HEADER = dict(
    SOAPACTION='"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"'
)

BODY = (
    '<?xml version="1.0"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap'
    '/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><'
    's:Body><u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1"><IRCCC'
    'ode>%s</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>'
)

NUMBERS = [
    'Num0'
    'Num1'
    'Num2'
    'Num3'
    'Num4'
    'Num5'
    'Num6'
    'Num7'
    'Num8'
    'Num9'
]
