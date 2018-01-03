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
        Audio source screen.

        **Getter:** Gets the current screen audio is playing from.

            *Returns:*

                * ``"main"`` - Main screen.
                * ``"sub"`` - PIP screen.

            *Return type:* `str`

        **Setter:** Sets the screen audio is playing from.

            *Accepted values:*

                * ``"main"`` - Main screen.
                * ``"sub"`` - PIP screen.

            *Value type:* `str`
        """
        return self.__send('getAudioSourceScreen')[0]['screen']

    @audio_source_screen.setter
    def audio_source_screen(self, value):
        self.__send('setAudioSourceScreen', screen=value)

    @property
    def banner_mode(self):
        """
        Banner mode.

        **Getter:** Gets the banner mode.

            *Returns:*

                * ``"large"`` - Long banner.
                * ``"small"`` - Short banner.
                * ``"hidden"`` - No banner displayed.

            *Return type:* `str`

        **Setter:** Sets the banner mode.

            *Accepted values:*

                * ``"large"`` - Long banner.
                * ``"small"`` - Short banner.
                * ``"hidden"`` - No banner displayed.

            *Value type:* `str`
        """

        return self.__send('getBannerMode')[0]['currentValue']

    @banner_mode.setter
    def banner_mode(self, value):
        self.__send('setBannerMode', value=value)

    @property
    def multi_screen_mode(self):
        """
        Banner mode.

        **Getter:** Gets the screen mode.

            *Returns:*

                * ``"single"`` - Single screen mode.
                * ``"PIP"`` - Picture In Picture mode.
                * ``"PAP"`` - Picture And Picture mode.
                * ``"widgetMode"`` - Picture and Widget application mode.
                * ``"internetPhoneMode"`` - Internet phone application mode.
                * ``"other"`` - Other mode.

            *Return type:* `str`

        **Setter:** Sets the screen mode.

            *Accepted values:*

                * ``"single"`` - Single screen mode.
                * ``"PIP"`` - Picture In Picture mode.
                * ``"PAP"`` - Picture And Picture mode.

            *Value type:* `str`
        """
        return self.__send('getMultiScreenMode')[0]['mode']

    @multi_screen_mode.setter
    def multi_screen_mode(self, value):
        self.__send('setMultiScreenMode', mode=value)

    @property
    def pip_position(self):
        """
        PIP screen position.

        **Getter:** Gets the PIP screen position.

            *Returns:*

                * ``"leftTop"`` - Upper left corner of main screen.
                * ``"leftBottom"`` - Lower left corner of main screen.
                * ``"rightTop"`` - Upper right corner of main screen.
                * ``"rightBottom"`` - Lower right corner of main screen.
                * ``"invalid"`` - Current Multi Screen Mode is not PIP.

            *Return type:* `str`

        **Setter:** Sets the PIP screen position.

            *Accepted values:*

                * ``"leftTop"`` - Upper left corner of main screen.
                * ``"leftBottom"`` - Lower left corner of main screen.
                * ``"rightTop"`` - Upper right corner of main screen.
                * ``"rightBottom"`` - Lower right corner of main screen.
                * ``"invalid"`` - Current Multi Screen Mode is not PIP.

            *Value type:* `str`
        """
        return self.__send('getPipSubScreenPosition')[0]['position']

    @pip_position.setter
    def pip_position(self, value):
        self.__send('setPipSubScreenPosition', position=value)

    @property
    def scene_setting(self):
        """
        Scene setting.

        **Getter:** Gets the scene setting.

            *Returns:*

                * ``"auto"`` - Automatically selects the scene based on the viewing content.
                * ``"auto24pSync"`` - Automatically selects "Cinema" for 24Hz signal content. Behaves as "Auto" for all other signals.
                * ``"general"`` - Turn off scene select for general content.
                * ``"cinema"`` - Optimal picture and sound for watching movies.
                * ``"sports"`` - Optimal picture and sound for watching sports.
                * ``"music"`` - Optimal sound for listening to music.
                * ``"animation"`` - Optimal picture for watching animation.
                * ``"photo"`` - Optimal picture for viewing photos.
                * ``"game"`` - Optimal picture and sound for playing video games.
                * ``"graphics"`` - Optimal picture for viewing tables and characters.

            *Return type:* `str`

        **Setter:** Sets the scene setting.

            *Accepted values:*

                * ``"auto"`` - Automatically selects the scene based on the viewing content.
                * ``"auto24pSync"`` - Automatically selects "Cinema" for 24Hz signal content. Behaves as "Auto" for all other signals.
                * ``"general"`` - Turn off scene select for general content.
                * ``"cinema"`` - Optimal picture and sound for watching movies.
                * ``"sports"`` - Optimal picture and sound for watching sports.
                * ``"music"`` - Optimal sound for listening to music.
                * ``"animation"`` - Optimal picture for watching animation.
                * ``"photo"`` - Optimal picture for viewing photos.
                * ``"game"`` - Optimal picture and sound for playing video games.
                * ``"graphics"`` - Optimal picture for viewing tables and characters.

            *Value type:* `str`

        """
        return self.__send('getPipSubScreenPosition')[0]['currentValue']

    @scene_setting.setter
    def scene_setting(self, value):
        self.__send('setPipSubScreenPosition', value=value)

    def pap_screen_size(self, screen, increment):
        """
        PAP screen size.

        :param str screen:
            *Accepted values:*

                * ``"main"`` - Main screen.
                * ``"sub"`` - Sub screen.

        :param int increment: The increment can be +- number.
            This number is the number of changes to take place. so if you do
            a +1 it will increase the size by one and a +2 will be increasing
            the size 2 steps. Same deal with - except making the size smaller.

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
