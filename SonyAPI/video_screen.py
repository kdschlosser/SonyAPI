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


class VideoScreen(object):

    def __init__(self, sony_api):
        self.__sony_api = sony_api

    def __send(self, method, **params):
        return self.__sony_api.send('videoScreen', method, **params)

    @property
    def audio_source_screen(self):
        """
        Gets the current screen audio is playing from.

        :return: Possible values:
            "main" - Main screen.
            "sub" - PIP screen.
        :rtype: str
        """

        return self.__send('getAudioSourceScreen')[0]['screen']

    @audio_source_screen.setter
    def audio_source_screen(self, value):
        """
        Sets the screen audio is playing from.

        :param value: Possible values:
            "main" - Main screen.
            "sub" - PIP screen.
        :type value: str
        :return: None
        :rtype: None
        """

        self.__send('setAudioSourceScreen', screen=value)

    @property
    def banner_mode(self):
        """
        Gets the banner mode.

        :return: Possible values:
            "large" - Long banner.
            "small" - Short banner.
            "hidden" - No banner displayed.
        :rtype: str
        """

        return self.__send('getBannerMode')[0]['currentValue']

    @banner_mode.setter
    def banner_mode(self, value):
        """
        Sets the banner mode.

        :param value: Possible values:
            "large" - Long banner.
            "small" - Short banner.
            "hidden" - No banner displayed.
        :type value: str
        :return: None
        :rtype: None
        """

        self.__send('setBannerMode', value=value)

    @property
    def multi_screen_mode(self):
        """
        Gets the screen mode.

        :return: Possible values:
            "single" - single screen mode
            "PIP" - Picture In Picture mode
            "PAP" - Picture And Picture mode
            "widgetMode" - Picture and Widget application mode
            "internetPhoneMode" - Internet Phone application mode
            "other" - other mode
        :rtype: str
        """
        return self.__send('getMultiScreenMode')[0]['mode']

    @multi_screen_mode.setter
    def multi_screen_mode(self, value):
        """
        Sets the screen mode.

        :param value: Possible values:
            "single" - single screen mode
            "PIP" - Picture In Picture mode
            "PAP" - Picture And Picture mode

        :type value: str
        :return: None
        :rtype: None
        """

        self.__send('setMultiScreenMode', mode=value)

    @property
    def pip_position(self):
        """
        Gets the PIP screen position.

        :return: Possible values:
            "leftTop" - shown in the upper left corner of main screen
            "leftBottom" - shown in the lower left corner of main screen
            "rightTop" - shown in the upper right corner of main screen
            "rightBottom" - shown in the lower right corner of main screen
            "invalid" - sub screen is not shown. That means the current Multi
            Screen Mode is not PIP.

        :rtype: str
        """
        return self.__send('getPipSubScreenPosition')[0]['position']

    @pip_position.setter
    def pip_position(self, value):
        """
        Sets the PIP screen position.

        :param value: Possible values:
            "leftTop" - shown in the upper left corner of main screen
            "leftBottom" - shown in the lower left corner of main screen
            "rightTop" - shown in the upper right corner of main screen
            "rightBottom" - shown in the lower right corner of main screen

        :type value: str
        :return: None
        :rtype: None
        """

        self.__send('setPipSubScreenPosition', position=value)

    @property
    def scene_setting(self):
        """
        Gets the scene setting.

        :return: Possible values:
            "auto" - Automatically selects the scene based on the viewing
            content.
            "auto24pSync" - Automatically selects "Cinema" for 24Hz signal
            content. Behaves as "Auto" for all other signals.
            "general" - Turn off scene select for general content.
            "cinema" - Optimal picture and sound for watching movies.
            "sports" - Optimal picture and sound for watching sports.
            "music" - Optimal sound for listening to music.
            "animation" - Optimal picture for watching animation.
            "photo" - Optimal picture for viewing photos.
            "game" - Optimal picture and sound for playing video games.
            "graphics" - Optimal picture for viewing tables and characters.
        :rtype: str
        """
        return self.__send('getPipSubScreenPosition')[0]['currentValue']

    @scene_setting.setter
    def scene_setting(self, value):
        """
        Sets the scene setting.

        :param value: Possible values:
            "auto" - Automatically selects the scene based on the viewing
            content.
            "auto24pSync" - Automatically selects "Cinema" for 24Hz signal
            content. Behaves as "Auto" for all other signals.
            "general" - Turn off scene select for general content.
            "cinema" - Optimal picture and sound for watching movies.
            "sports" - Optimal picture and sound for watching sports.
            "music" - Optimal sound for listening to music.
            "animation" - Optimal picture for watching animation.
            "photo" - Optimal picture for viewing photos.
            "game" - Optimal picture and sound for playing video games.
            "graphics" - Optimal picture for viewing tables and characters.
        :type value: str
        :return: None
        :rtype: None
        """

        self.__send('setPipSubScreenPosition', value=value)

    def pap_screen_size(self, screen, increment):
        """
        Sets the PAP screen size.

        :param screen: Possible values:
            "main" - main screen
            "sub" - sub screen
        :type screen: str

        :param increment: The increment can be + or -. This number is the
        number of changes to take place. so if yo9u do a +1 it will increase
        the size by one and a +2 will be increasing the size 2 steps.
        Same deal with - except making the size smaller.
        :type increment: int

        :return: None
        :rtype: None
        """

        if increment < 0:
            self.__send('setPapScreenSize', screen=screen, size=str(increment))
        else:
            self.__send(
                'setPapScreenSize',
                screen=screen,
                size='+' + str(increment)
            )
