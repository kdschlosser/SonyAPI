# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.


class BroadcastLink(object):
    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, method, **params):
        return self.__sony_api('broadcastLink', method, **params)[0]

    @property
    def server_info(self):
        """
        Gets information of broadcastLink server.

        :return: dictionary
            "broadcastType": Broadcast type.
                "arib" - Japanese broadcast.
                "isdbg" - Brazil broadcast.

            "specVersion": BroadcastLink specification version.
                "phase0" - specification phase 0.
                "phase1" - specification phase 1.
        :rtype: dict
        """
        return self.__send('getBroadcastLinkServerInfo')[0]

    def send_message(self, uuid, message):
        """

        :param uuid: UUID of companion device.
        :type uuid: str

        :param message: Message from a companion device's (client) web
            application to a broadcast link server.
        :type message: str

        :return: None
        :rtype: None
        """

        self.__send('sendMessage', uuid=uuid, message=message)

    def connection_mode(self, uuid, connection):
        """
        Declare client's connection state to broadcastlink server.

        Server regards client as connected until time passed (timeoutSec)
        specified in the response.

        :param uuid: UUID of companion device.
        :type uuid: str
        :param connection: A client is connected or not.
            True - connected.
            False - disconnected.

        :type connection: bool
        :return: timeoutSec
        :rtype: int
        """
        return self.__send(
            'setConnectionMode',
            uuid=uuid,
            connection=connection
        )[0]['timeoutSec']
