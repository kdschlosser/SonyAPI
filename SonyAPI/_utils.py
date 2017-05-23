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


def get_mac_address(ip_address):
    send_arp = ctypes.windll.Iphlpapi.SendARP
    inetaddr = ctypes.windll.wsock32.inet_addr(ip_address)

    hw_address = ctypes.c_buffer(6)
    addlen = ctypes.c_ulong(ctypes.sizeof(hw_address))

    send_arp(inetaddr, 0, ctypes.byref(hw_address), ctypes.byref(addlen))

    for val in struct.unpack('BBBBBB', hw_address):
        if val > 15:
            replace_str = '0x'
        else:
            replace_str = 'x'

        yield hex(val).replace(replace_str, '').upper()

    return
