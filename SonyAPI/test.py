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

from __future__ import print_function
import traceback

try:
    Error = getattr(__import__('__builtin__'), 'Exception')
except ImportError:
    Error = getattr(__import__('builtins.Exception'), 'Exception')

ATTR_NAMES = (
    'audio_channel',
    'audio_codec',
    'audio_frequency',
    'bivl_asset_id',
    'bivl_provider',
    'bivl_service_id',
    'channel_name',
    'channel_surfing_visibility',
    'chapter_count',
    'connection',
    'content_type',
    'created_time',
    'data',
    'direct_remote_num',
    'display_icon',
    'display_num',
    'duration',
    'elapsed',
    'end_time',
    'epg_visibility',
    'file_size_byte',
    'icon',
    'id',
    'idx',
    'index',
    'is_already_played',
    'is_protected',
    'label',
    'media_type',
    'original_display_num',
    'overlap_status',
    'parental_country',
    'parental_rating',
    'parental_system',
    'percent_elapsed',
    'play_speed',
    'product_id',
    'program_media_type',
    'program_num',
    'program_title',
    'quality',
    'reason_id',
    'reason_msg',
    'remaining',
    'repeat_type',
    'size_mb',
    'source',
    'start_time',
    'status',
    'storage_uri',
    'subtitle_language',
    'subtitle_title',
    'title',
    'triplet_str',
    'type',
    'uri',
    'user_content_flag',
    'video_codec',
    'visibility'
)

SONY_API = None


def print_single(attr_name):
    try:
        print('%s: %r' % (attr_name, getattr(SONY_API, attr_name)))
    except SONY_API.UnsupportedError:
        print('%s: NOT SUPPORTED' % attr_name)
    except Error:
        print('%s: %s' % (attr_name, traceback.format_exc()))


def print_multiple(item, label, attr_names):
    found_names = []
    for attr_name in attr_names:
        if hasattr(item, attr_name):
            try:
                print(
                    '    %s.%s: %r' %
                    (label, attr_name, getattr(item, attr_name))
                )
                found_names += [attr_name]
            except Error:
                print(
                    '    %s.%s: %s' %
                    (label, attr_name, traceback.format_exc())
                )
    return found_names


def p(*args):
    if len(args) == 1:
        print_single(args[0])
    else:
        label, attrs = args
        found_names = []

        try:
            for attr in attrs:
                if found_names:
                    print_multiple(attr, label, found_names)

                else:
                    print_multiple(attr, label, ATTR_NAMES)
                print('-' * 80)
        except TypeError:
            print_multiple(attrs, label, ATTR_NAMES)


class TestAPI(object):
    _sony_api = None

    def __init__(self):

        import SonyAPI
        import sys

        # SonyAPI._LOGGER.file_writer = sys.stdout.write

        def build_command_list(self):
            pass

        def discover(self, timeout=10):
            return ['192.168.1.2']

        def get_pin(self):
            return self._pin

        def set_pin(self, pin):
            self._pin = pin

        def send(self, protocol, method, return_index=0, **params):
            result = TEST_SCHEMA[protocol][method]['result'][return_index]
            return result

        SonyAPI.SonyAPI.send = send
        SonyAPI.SonyAPI.discover = discover
        SonyAPI.SonyAPI._build_command_list = build_command_list
        SonyAPI.SonyAPI.pin = property(fget=get_pin, fset=set_pin)
        api = SonyAPI.SonyAPI(ip_address='192.168.1.2', pin=1234)
        api.run_tests()


def run(sony_api):
    global SONY_API
    SONY_API = sony_api
    sony_api.cache_icons()

    print('sony_api.discover:', sony_api.discover())
    print('=' * 80)
    print()

    p('model')
    p('serial')
    p('name')
    p('generation')
    p('product')
    p('remote_model')
    p('cid')
    p('mac')
    p('wol_mac')
    p('wol_mode')
    p('postal_code')
    p('language')
    print('=' * 80)
    print()

    p('time_format')
    p('date_format')
    p('time')
    print('=' * 80)
    print()

    p('network_ipv4')
    p('network_netif')
    p('network_ipv6')
    p('network_subnet_mask')
    p('network_dns')
    p('network_mac')
    p('network_gateway')
    print('=' * 80)
    print()

    p('interface_server_name')
    p('interface_model_name')
    p('interface_product_name')
    p('interface_product_category')
    p('interface_version')
    print('=' * 80)
    print()

    p('parental_rating_setting_country')
    p('parental_rating_setting_unrated')
    p('parental_rating_setting_age')
    p('parental_rating_setting_sony')
    p('parental_rating_setting_tv')
    p('parental_rating_setting_mpaa')
    p('parental_rating_setting_french')
    p('parental_rating_setting_english')
    print('=' * 80)
    print()

    p('led_indicator_status')
    p('recording_status')
    # p('remote_device_settings')
    p('browser_text_url')
    print('=' * 80)
    print()

    p('power_saving_mode')
    p('chinese_software_keyboard_supported')
    p('color_keys_layout')
    p('pip_sub_screen_position')
    p('audio_source_screen')
    p('multi_screen_mode')
    p('multi_screen_internet_mode')
    p('recording_supported_repeat_type')
    p('command_list')
    print('=' * 80)
    print()

    print('volume:')
    speaker = sony_api.volume.speaker
    print('    volume:', speaker, '%')
    speaker.up()
    print('    volume:', speaker, '%')
    speaker.down()
    print('    volume:', speaker, '%')
    speaker += 1
    print('    volume:', speaker, '%')
    speaker -= 1
    print('    volume:', speaker, '%')
    print('=' * 80)
    print()

    print('mute:')
    print('    mute:', speaker.mute)
    speaker.mute = True
    print('    mute:', speaker.mute)
    speaker.mute = False
    print('    mute:', speaker.mute)
    print('=' * 80)
    print()

    print('channel:')
    channel = sony_api.channel
    try:
        print('    channel:', channel)
        speaker.up()
        print('    channel:', channel)
    except Error:
        print('    channel:', traceback.format_exc())
    try:
        speaker.down()
        print('    channel:', channel)
    except Error:
        print('    channel:', traceback.format_exc())
    try:
        speaker += 1
        print('    channel:', channel)
    except Error:
        print('    channel:', traceback.format_exc())
    try:
        speaker -= 1
        print('    channel:', channel)
    except Error:
        print('    channel:', traceback.format_exc())
    print('=' * 80)
    print()

    try:
        items = sony_api.scheme_list
        print('scheme_list:')
        for item in items:
            print('    scheme:', repr(item))
    except SONY_API.UnsupportedError:
        print('scheme_list: NOT SUPPORTED')
    except Error:
        print('scheme_list: %s' % traceback.format_exc())
    print('=' * 80)
    print()

    try:
        items = sony_api.application_status_list
        print('application_status_list:')
        for item in items:
            print('    name, status:', item)
    except SONY_API.UnsupportedError:
        print('application_status_list: NOT SUPPORTED')
    except Error:
        print('application_status_list: %s' % traceback.format_exc())
    print('=' * 80)
    print()

    try:
        items = sony_api.content_count
        print('content_count:')
        for item in items:
            print('    inputs.InputItem, count:', item)
    except SONY_API.UnsupportedError:
        print('content_count: NOT SUPPORTED')
    except Error:
        print('content_count: %s' % traceback.format_exc())
    print('=' * 80)
    print()

    try:
        items = sony_api.browser_bookmark_list
        print('browser_bookmark_list:')
        p('browser.BookmarkItem', items)
    except SONY_API.UnsupportedError:
        print('browser_bookmark_list: NOT SUPPORTED')
    except Error:
        print('browser_bookmark_list: %s' % traceback.format_exc())
    print('=' * 80)
    print()

    try:
        items = sony_api.source_list
        print('source_list:')
        p('inputs.InputItem', items)
    except SONY_API.UnsupportedError:
        print('browser_bookmark_list: NOT SUPPORTED')
    except Error:
        print('browser_bookmark_list: %s' % traceback.format_exc())
    print('=' * 80)
    print()

    try:
        items = sony_api.application_list
        print('application_list:')
        p('application.Application', items)
    except SONY_API.UnsupportedError:
        print('browser_bookmark_list: NOT SUPPORTED')
    except Error:
        print('browser_bookmark_list: %s' % traceback.format_exc())
    print('=' * 80)
    print()

    try:
        items = sony_api.recording_history_list
        print('recording_history_list:')
        p('recording.HistoryItem', items)
    except SONY_API.UnsupportedError:
        print('browser_bookmark_list: NOT SUPPORTED')
    except Error:
        print('browser_bookmark_list: %s' % traceback.format_exc())
    print('=' * 80)
    print()

    try:
        items = sony_api.recording_schedule_list
        print('recording_schedule_list:')
        p('recording.ScheduleItem', items)
    except SONY_API.UnsupportedError:
        print('browser_bookmark_list: NOT SUPPORTED')
    except Error:
        print('browser_bookmark_list: %s' % traceback.format_exc())
    print('=' * 80)
    print()

    try:
        items = sony_api.recording_conflict_list
        print('recording_conflict_list:')
        p('recording.ScheduleItem:', items)
    except SONY_API.UnsupportedError:
        print('browser_bookmark_list: NOT SUPPORTED')
    except Error:
        print('browser_bookmark_list: %s' % traceback.format_exc())
    print('=' * 80)
    print()

    try:
        items = sony_api.content_list
        print('content_list:')
        p('media.ContentItem', items)
    except SONY_API.UnsupportedError:
        print('browser_bookmark_list: NOT SUPPORTED')
    except Error:
        print('browser_bookmark_list: %s' % traceback.format_exc())
    print('=' * 80)
    print()

    try:
        items = sony_api.now_playing
        print('now_playing:')
        p('media.NowPlaying', items)
    except SONY_API.UnsupportedError:
        print('browser_bookmark_list: NOT SUPPORTED')
    except Error:
        print('browser_bookmark_list: %s' % traceback.format_exc())
    print('=' * 80)
    print()
    print('DONE!')


TEST_SCHEMA = {
    "system": {
        "getLEDIndicatorStatus": {
            "params": ["1.2"],
            "result": [
                {
                    "status": "",
                    "mode": ""
                }
            ]
        },
        "setLEDIndicatorStatus": {
            "params": [
                {
                    "status": "",
                    "mode": ""
                }
            ],
            "result": []
        },
        "requestReboot": {
            "params": [
                "1.0"
            ],
            "result": []
        },
        "getPowerStatus": {
            "params": [
                "1.0"
            ],
            "result": [
                {
                    "status": "active"
                }
            ]
        },
        "setCurrentTime": {
            "params": [
                {
                "dateTime": ""
                }
            ],
            "result": []
        },
        "getPowerSavingMode": {
            "params": [
                "1.0"
            ],
            "result": [
                {
                    "mode": "off"
                }
            ]
        },
        "getInterfaceInformation": {
            "params": [
                "1.0"
            ],
            "result": [
                {
                    "serverName": "",
                    "modelName": "KDL-40W605B",
                    "productName": "BRAVIA",
                    "productCategory": "tv",
                    "interfaceVersion": "2.3.0"
                }
            ]
        },
        "getVersions": {
            "params": [],
            "result": [["1.0"]]
        },
        "setPowerStatus": {
            "params": [
                {
                    "status": False
                }
            ],
            "result": []
        },
        "getWolMode": {
            "params": [
                "1.0"
            ],
            "result": [
                {
                    "enabled": True
                }
            ]
        },
        "setWolMode": {
            "params": [
                {
                    "enabled": True
                }
            ],
            "result": []
        },
        "setLanguage": {
            "params": [
                {
                    "language": "EN"
                }

            ],
            "result": []
        },
        "getCurrentTime": {
            "params": [
                "1.0"
            ],
            "result": [
                "2014-10-16T00:55:22+0400"
            ]
        },
        "getSystemInformation": {
            "params": [
                "1.0"
            ],
            "result": [
                {
                    "product": "TV",
                    "macAddr": "11:22:33:44:55:66",
                    "name": "BRAVIA",
                    "language": "rus",
                    "area": "RUS",
                    "generation": "2.3.0",
                    "model": "KDL-40W605B",
                    "cid": "1234",
                    "region": "RUS",
                    "serial": "12345677889"
                }
            ]
        },
        "getSystemSupportedFunction": {
            "params": [
                "1.0"
            ],
            "result": [
                [
                    {
                        "option": "WOL",
                        "value": "11:22:33:44:55:66"
                    },
                    {
                        "option": "SupportedChineseSoftwareKeyboard",
                        "value": "no"
                    }
                ]
            ]
        },
        "getPostalCode": {
            "params": [
                "1.0"
            ],
            "result": [
                {
                    "postalCode": "80134"
                }
            ]
        },
        "setPostalCode": {
            "params": [
                {
                    "postalCode": "80134"
                }
            ],
            "result": []
        },
        "getRemoteControllerInfo": {
            "params": [
                "1.0"
            ],
            "result": [
                {
                    "bundled": True,
                    "type": "RM-J1100"
                },
                [
                    {
                        "name": "PowerOff",
                        "value": "AAAAAQAAAAEAAAAvAw=="
                    },
                    {
                        "name": "Input",
                        "value": "AAAAAQAAAAEAAAAlAw=="
                    },
                    {
                        "name": "GGuide",
                        "value": "AAAAAQAAAAEAAAAOAw=="
                    },
                    {
                        "name": "EPG",
                        "value": "AAAAAgAAAKQAAABbAw=="
                    },
                    {
                        "name": "Favorites",
                        "value": "AAAAAgAAAHcAAAB2Aw=="
                    },
                    {
                        "name": "Display",
                        "value": "AAAAAQAAAAEAAAA6Aw=="
                    },
                    {
                        "name": "Home",
                        "value": "AAAAAQAAAAEAAABgAw=="
                    },
                    {
                        "name": "Options",
                        "value": "AAAAAgAAAJcAAAA2Aw=="
                    },
                    {
                        "name": "Return",
                        "value": "AAAAAgAAAJcAAAAjAw=="
                    },
                    {
                        "name": "Up",
                        "value": "AAAAAQAAAAEAAAB0Aw=="
                    },
                    {
                        "name": "Down",
                        "value": "AAAAAQAAAAEAAAB1Aw=="
                    },
                    {
                        "name": "Right",
                        "value": "AAAAAQAAAAEAAAAzAw=="
                    },
                    {
                        "name": "Left",
                        "value": "AAAAAQAAAAEAAAA0Aw=="
                    },
                    {
                        "name": "Confirm",
                        "value": "AAAAAQAAAAEAAABlAw=="
                    },
                    {
                        "name": "Red",
                        "value": "AAAAAgAAAJcAAAAlAw=="
                    },
                    {
                        "name": "Green",
                        "value": "AAAAAgAAAJcAAAAmAw=="
                    },
                    {
                        "name": "Yellow",
                        "value": "AAAAAgAAAJcAAAAnAw=="
                    },
                    {
                        "name": "Blue",
                        "value": "AAAAAgAAAJcAAAAkAw=="
                    },
                    {
                        "name": "Num1",
                        "value": "AAAAAQAAAAEAAAAAAw=="
                    },
                    {
                        "name": "Num2",
                        "value": "AAAAAQAAAAEAAAABAw=="
                    },
                    {
                        "name": "Num3",
                        "value": "AAAAAQAAAAEAAAACAw=="
                    },
                    {
                        "name": "Num4",
                        "value": "AAAAAQAAAAEAAAADAw=="
                    },
                    {
                        "name": "Num5",
                        "value": "AAAAAQAAAAEAAAAEAw=="
                    },
                    {
                        "name": "Num6",
                        "value": "AAAAAQAAAAEAAAAFAw=="
                    },
                    {
                        "name": "Num7",
                        "value": "AAAAAQAAAAEAAAAGAw=="
                    },
                    {
                        "name": "Num8",
                        "value": "AAAAAQAAAAEAAAAHAw=="
                    },
                    {
                        "name": "Num9",
                        "value": "AAAAAQAAAAEAAAAIAw=="
                    },
                    {
                        "name": "Num0",
                        "value": "AAAAAQAAAAEAAAAJAw=="
                    },
                    {
                        "name": "Num11",
                        "value": "AAAAAQAAAAEAAAAKAw=="
                    },
                    {
                        "name": "Num12",
                        "value": "AAAAAQAAAAEAAAALAw=="
                    },
                    {
                        "name": "VolumeUp",
                        "value": "AAAAAQAAAAEAAAASAw=="
                    },
                    {
                        "name": "VolumeDown",
                        "value": "AAAAAQAAAAEAAAATAw=="
                    },
                    {
                        "name": "Mute",
                        "value": "AAAAAQAAAAEAAAAUAw=="
                    },
                    {
                        "name": "ChannelUp",
                        "value": "AAAAAQAAAAEAAAAQAw=="
                    },
                    {
                        "name": "ChannelDown",
                        "value": "AAAAAQAAAAEAAAARAw=="
                    },
                    {
                        "name": "SubTitle",
                        "value": "AAAAAgAAAJcAAAAoAw=="
                    },
                    {
                        "name": "ClosedCaption",
                        "value": "AAAAAgAAAKQAAAAQAw=="
                    },
                    {
                        "name": "Enter",
                        "value": "AAAAAQAAAAEAAAALAw=="
                    },
                    {
                        "name": "DOT",
                        "value": "AAAAAgAAAJcAAAAdAw=="
                    },
                    {
                        "name": "Analog",
                        "value": "AAAAAgAAAHcAAAANAw=="
                    },
                    {
                        "name": "Teletext",
                        "value": "AAAAAQAAAAEAAAA/Aw=="
                    },
                    {
                        "name": "Exit",
                        "value": "AAAAAQAAAAEAAABjAw=="
                    },
                    {
                        "name": "Analog2",
                        "value": "AAAAAQAAAAEAAAA4Aw=="
                    },
                    {
                        "name": "*AD",
                        "value": "AAAAAgAAABoAAAA7Aw=="
                    },
                    {
                        "name": "Digital",
                        "value": "AAAAAgAAAJcAAAAyAw=="
                    },
                    {
                        "name": "Analog?",
                        "value": "AAAAAgAAAJcAAAAuAw=="
                    },
                    {
                        "name": "BS",
                        "value": "AAAAAgAAAJcAAAAsAw=="
                    },
                    {
                        "name": "CS",
                        "value": "AAAAAgAAAJcAAAArAw=="
                    },
                    {
                        "name": "BSCS",
                        "value": "AAAAAgAAAJcAAAAQAw=="
                    },
                    {
                        "name": "Ddata",
                        "value": "AAAAAgAAAJcAAAAVAw=="
                    },
                    {
                        "name": "PicOff",
                        "value": "AAAAAQAAAAEAAAA+Aw=="
                    },
                    {
                        "name": "Tv_Radio",
                        "value": "AAAAAgAAABoAAABXAw=="
                    },
                    {
                        "name": "Theater",
                        "value": "AAAAAgAAAHcAAABgAw=="
                    },
                    {
                        "name": "SEN",
                        "value": "AAAAAgAAABoAAAB9Aw=="
                    },
                    {
                        "name": "InternetWidgets",
                        "value": "AAAAAgAAABoAAAB6Aw=="
                    },
                    {
                        "name": "InternetVideo",
                        "value": "AAAAAgAAABoAAAB5Aw=="
                    },
                    {
                        "name": "Netflix",
                        "value": "AAAAAgAAABoAAAB8Aw=="
                    },
                    {
                        "name": "SceneSelect",
                        "value": "AAAAAgAAABoAAAB4Aw=="
                    },
                    {
                        "name": "Mode3D",
                        "value": "AAAAAgAAAHcAAABNAw=="
                    },
                    {
                        "name": "iManual",
                        "value": "AAAAAgAAABoAAAB7Aw=="
                    },
                    {
                        "name": "Audio",
                        "value": "AAAAAQAAAAEAAAAXAw=="
                    },
                    {
                        "name": "Wide",
                        "value": "AAAAAgAAAKQAAAA9Aw=="
                    },
                    {
                        "name": "Jump",
                        "value": "AAAAAQAAAAEAAAA7Aw=="
                    },
                    {
                        "name": "PAP",
                        "value": "AAAAAgAAAKQAAAB3Aw=="
                    },
                    {
                        "name": "MyEPG",
                        "value": "AAAAAgAAAHcAAABrAw=="
                    },
                    {
                        "name": "ProgramDescription",
                        "value": "AAAAAgAAAJcAAAAWAw=="
                    },
                    {
                        "name": "WriteChapter",
                        "value": "AAAAAgAAAHcAAABsAw=="
                    },
                    {
                        "name": "TrackID",
                        "value": "AAAAAgAAABoAAAB+Aw=="
                    },
                    {
                        "name": "TenKey",
                        "value": "AAAAAgAAAJcAAAAMAw=="
                    },
                    {
                        "name": "AppliCast",
                        "value": "AAAAAgAAABoAAABvAw=="
                    },
                    {
                        "name": "acTVila",
                        "value": "AAAAAgAAABoAAAByAw=="
                    },
                    {
                        "name": "DeleteVideo",
                        "value": "AAAAAgAAAHcAAAAfAw=="
                    },
                    {
                        "name": "PhotoFrame",
                        "value": "AAAAAgAAABoAAABVAw=="
                    },
                    {
                        "name": "TvPause",
                        "value": "AAAAAgAAABoAAABnAw=="
                    },
                    {
                        "name": "KeyPad",
                        "value": "AAAAAgAAABoAAAB1Aw=="
                    },
                    {
                        "name": "Media",
                        "value": "AAAAAgAAAJcAAAA4Aw=="
                    },
                    {
                        "name": "SyncMenu",
                        "value": "AAAAAgAAABoAAABYAw=="
                    },
                    {
                        "name": "Forward",
                        "value": "AAAAAgAAAJcAAAAcAw=="
                    },
                    {
                        "name": "Play",
                        "value": "AAAAAgAAAJcAAAAaAw=="
                    },
                    {
                        "name": "Rewind",
                        "value": "AAAAAgAAAJcAAAAbAw=="
                    },
                    {
                        "name": "Prev",
                        "value": "AAAAAgAAAJcAAAA8Aw=="
                    },
                    {
                        "name": "Stop",
                        "value": "AAAAAgAAAJcAAAAYAw=="
                    },
                    {
                        "name": "Next",
                        "value": "AAAAAgAAAJcAAAA9Aw=="
                    },
                    {
                        "name": "Rec",
                        "value": "AAAAAgAAAJcAAAAgAw=="
                    },
                    {
                        "name": "Pause",
                        "value": "AAAAAgAAAJcAAAAZAw=="
                    },
                    {
                        "name": "Eject",
                        "value": "AAAAAgAAAJcAAABIAw=="
                    },
                    {
                        "name": "FlashPlus",
                        "value": "AAAAAgAAAJcAAAB4Aw=="
                    },
                    {
                        "name": "FlashMinus",
                        "value": "AAAAAgAAAJcAAAB5Aw=="
                    },
                    {
                        "name": "TopMenu",
                        "value": "AAAAAgAAABoAAABgAw=="
                    },
                    {
                        "name": "PopUpMenu",
                        "value": "AAAAAgAAABoAAABhAw=="
                    },
                    {
                        "name": "RakurakuStart",
                        "value": "AAAAAgAAAHcAAABqAw=="
                    },
                    {
                        "name": "OneTouchTimeRec",
                        "value": "AAAAAgAAABoAAABkAw=="
                    },
                    {
                        "name": "OneTouchView",
                        "value": "AAAAAgAAABoAAABlAw=="
                    },
                    {
                        "name": "OneTouchRec",
                        "value": "AAAAAgAAABoAAABiAw=="
                    },
                    {
                        "name": "OneTouchStop",
                        "value": "AAAAAgAAABoAAABjAw=="
                    },
                    {
                        "name": "DUX",
                        "value": "AAAAAgAAABoAAABzAw=="
                    },
                    {
                        "name": "FootballMode",
                        "value": "AAAAAgAAABoAAAB2Aw=="
                    },
                    {
                        "name": "Social",
                        "value": "AAAAAgAAABoAAAB0Aw=="
                    }
                ]
            ]
        },
        "getColorKeysLayout": {
            "params": [
                "1.0"
            ],
            "result": [
                {
                    "colorKeysLayout": "RGYB"
                }
            ]
        },
        "setPowerSavingMode": {
            "params": [
                {
                    "status": False
                }
            ],
            "result": []
        },
        "getDateTimeFormat": {
            "params": [
                "1.0"
            ],
            "result": [
                {
                    "timeFormat": "HH:mm",
                    "dateFormat": "E dd MMM yyyy"
                }
            ]
        },
        "getNetworkSettings": {
            "params": [
                "1.0"
            ],
            "result": [
                {
                    "auth_url": {
                        "default": "http://192.168.1.2/sony/webauth/auth_default"
                    },
                    "ipAddrV4": "192.168.1.2",
                    "netif": "",
                    "ipAddrV6": "",
                    "netmask": "255.255.255.0",
                    "dns": [
                        "8.8.8.8",
                        "8.8.4.4"
                    ],
                    "hwAddr": "11:22:33:44:55:66",
                    "gateway": "192.168.1.1"
                }
            ]
        }
    },
    "recording": {
        "getScheduleList": {
            "params": [],
            "result": [[]]
        },
        "getSupportedRepeatType": {
            "params": [
                "1.0"
            ],
            "result": [
                [
                    "1",
                    "d",
                    "w1",
                    "w2",
                    "w3",
                    "w4",
                    "w5",
                    "w6",
                    "w7",
                    "w15",
                    "w26",
                    "w16"
                ]
            ]
        },
        "getHistoryList": {
            "params": [],
            "result": [[]]
        },
        "deleteSchedule": {
            "params": [],
            "result": []
        },
        "addSchedule": {
            "params": [],
            "result": []
        },
        "getRecordingStatus": {
            "params": [
                "1.0"
            ],
            "result": [
                {
                    "status": "notStarted"
                }
            ]
        },
        "getConflictScheduleList": {
            "params": [],
            "result": []
        }
    },
    "videoScreen": {
        "getPipSubScreenPosition": {
            "params": [
                "1.0"
            ],
            "result": [
                {
                    "position": "invalid"
                }
            ]
        },
        "setPipSubScreenPosition": {
            "params": [
                {
                    "position": ""
                }
            ],
            "result": []
        },
        "setMultiScreenMode": {
            "params": [
                {
                    "mode": ""
                }
            ],
            "result": []
        },
        "getBannerMode": {
            "params": ["1.2"],
            "result": [
                {
                    "value": ""
                }
            ]
        },
        "setBannerMode": {
            "params": [
                {
                    "value": ""
                }
            ],
            "result": []
        },
        "getSceneSetting": {
            "params": ["1.2"],
            "result": [
                {
                    "value": ""
                }
            ]
        },
        "setSceneSetting": {
            "params": [
                {
                    "value": ""
                }
            ],
            "result": []
        },
        "setPapScreenSize": {
            "params": [
                {
                    "screen": "",
                    "size": ""
                }
            ],
            "result": []
        },
        "getMultiScreenMode": {
            "params": [
                "1.1"
            ],
            "result": [
                {
                    "mode": "single",
                    "option": {
                        "internetTVMode": False
                    }
                }
            ]
        },
        "getAudioSourceScreen": {
            "params": [
                "1.0"
            ],
            "result": [
                {
                    "screen": "main"
                }
            ]
        },
        "setAudioSourceScreen": {
            "params": [
                {
                    "screen": "main"
                }
            ],
            "result": []
        }
    },
    "avContent": {
        "getCurrentExternalInputsStatus": {
            "params": [
                "1.0"
            ],
            "result": [
                [
                    {
                        "title": "HDMI 1/MHL",
                        "connection": True,
                        "label": "",
                        "uri": "extInput:hdmi?port=1",
                        "icon": "meta:hdmi"
                    },
                    {
                        "title": "HDMI 2",
                        "connection": False,
                        "label": "",
                        "uri": "extInput:hdmi?port=2",
                        "icon": "meta:hdmi"
                    },
                    {
                        "title": "HDMI 3",
                        "connection": False,
                        "label": "",
                        "uri": "extInput:hdmi?port=3",
                        "icon": "meta:hdmi"
                    },
                    {
                        "title": "HDMI 4",
                        "connection": False,
                        "label": "",
                        "uri": "extInput:hdmi?port=4",
                        "icon": "meta:hdmi"
                    },
                    {
                        "title": "AV1",
                        "connection": False,
                        "label": "",
                        "uri": "extInput:scart?port=1",
                        "icon": "meta:scart"
                    },
                    {
                        "title": "AV2/Component",
                        "connection": False,
                        "label": "",
                        "uri": "extInput:composite?port=1",
                        "icon": "meta:component"
                    },
                    {
                        "title": "\u00d0\u0178\u00d0\u00bb\u00d0\u00b5\u00d0\u00b9\u00d0\u00b5\u00d1\u20ac 2",
                        "connection": True,
                        "label": "PlayStation 4",
                        "uri": "extInput:cec?type=player&port=2",
                        "icon": "meta:playbackdevice"
                    },
                    {
                        "title": "\u00d0\u201d\u00d1\u0192\u00d0\u00b1\u00d0\u00bb\u00d0\u00b8\u00d1\u20ac\u00d0\u00be\u00d0\u00b2\u00d0\u00b0\u00d0\u00bd\u00d0\u00b8\u00d0\u00b5 \u00d1\u008d\u00d0\u00ba\u00d1\u20ac\u00d0\u00b0\u00d0\u00bd\u00d0\u00b0",
                        "connection": False,
                        "label": "",
                        "uri": "extInput:widi?port=1",
                        "icon": "meta:wifidisplay"
                    },
                ]
            ]
        },
        "getParentalRatingSettings": {
            "params": [
                "1.0"
            ],
            "result": [
                {
                    "ratingTypeAge": -1,
                    "ratingCountry": "",
                    "unratedLock": "",
                    "ratingTypeSony": "",
                    "ratingCustomTypeTV": "",
                    "ratingCustomTypeMpaa": "",
                    "ratingCustomTypeCaFrench": "",
                    "ratingCustomTypeCaEnglish": ""
                }
            ]
        },
        "setPlayContent": {
            "params": [
                {
                    "uri": "extInput:hdmi?port=1"
                }
            ],
            "result": []
        },
        "getPlayingContentInfo": {
            "params": [
                "1.0"
            ],
            "result": [
                {
                    "bivl_provider": "",
                    "programNum": "",
                    "mediaType": "",
                    "originalDispNum": "",
                    "bivl_assetId": "",
                    "bivl_serviceId": "",
                    "playSpeed": "",
                    "tripletStr": "8835.11.2010",
                    "source": "tv:dvbt",
                    "programTitle": "\u00d0\u0178\u00d0\u00bb\u00d0\u00be\u00d1\u2026\u00d0\u00be\u00d0\u00b9 \u00d0\u00a1\u00d0\u00b0\u00d0\u00bd\u00d1\u201a\u00d0\u00b0",
                    "dispNum": "011",
                    "startDateTime": "2014-10-16T01:45:00+0400",
                    "title": "11 \u00d0 \u00d0\u2022\u00d0\u009d \u00d0\u00a2\u00d0\u2019",
                    "programMediaType": "tv",
                    "durationSec": 6300,
                    "uri": "tv:dvbt?trip=8835.11.2010&srvName=11%20%D0%A0%D0%95%D0%9D%20%D0%A2%D0%92"
                }
            ]
        },
        "setPlayTvContent": {
            "params": [
                {
                    "channel": ""
                }
            ],
            "result": []
        },
        "setDeleteProtection": {
            "params": [
                {
                    "isProtected": True,
                    "uri": ""

                }
            ],
            "result": []
        },
        "getContentList": {
            "params": [
                {
                    "source": "tv:dvbt",
                    "cnt": 50,
                    "type": "",
                    "target": "",
                    "stIdx": ""
                }
            ],
            "result": [
                [
                    {
                        "directRemoteNum": '',
                        "isProtected": False,
                        "isAlreadyPlayed": False,
                        "durationSec": 6300,
                        "programNum": '',
                        "originalDispNum": '',
                        "startDateTime": '"2014-10-16T01:45:00+0400"',
                        "channelName": '',
                        "source": '',
                        "userContentFlag": '',
                        "createdTime": '',
                        "sizeMb": '',
                        "parentalCountry": '',
                        "parentalSystem": '',
                        "parentalRating": '',
                        "subtitleTitle": '',
                        "subtitleLanguage": '',
                        "audioChannel": '',
                        "audioFrequency": '',
                        "audioCodec": '',
                        "chapterCount": '',
                        "videoCodec": '',
                        "storageUri": '',
                        "contentType": '',
                        "productId": '',
                        "fileSizeByte": '',
                        "visibility": '',
                        "channelSurfingVisibility": '',
                        "epgVisibility": '',
                        "idx": '',
                        "status": '',
                        "index": 0,
                        "tripletStr": "8835.1.1010",
                        "title": "01 \u00d0\u0178\u00d0\u2022\u00d0 \u00d0\u2019\u00d0\u00ab\u00d0\u2122 \u00d0\u0161\u00d0\u0090\u00d0\u009d\u00d0\u0090\u00d0\u203a",
                        "uri": "tv:dvbt?trip=8835.1.1010&srvName=01%20%D0%9F%D0%95%D0%A0%D0%92%D0%AB%D0%99%20%D0%9A%D0%90%D0%9D%D0%90%D0%9B",
                        "dispNum": "001",
                        "programMediaType": "tv"
                    },
                    {
                        "directRemoteNum": '',
                        "isProtected": False,
                        "isAlreadyPlayed": False,
                        "durationSec": 6300,
                        "programNum": '',
                        "originalDispNum": '',
                        "startDateTime": '"2014-10-16T01:45:00+0400"',
                        "channelName": '',
                        "source": '',
                        "userContentFlag": '',
                        "createdTime": '',
                        "sizeMb": '',
                        "parentalCountry": '',
                        "parentalSystem": '',
                        "parentalRating": '',
                        "subtitleTitle": '',
                        "subtitleLanguage": '',
                        "audioChannel": '',
                        "audioFrequency": '',
                        "audioCodec": '',
                        "chapterCount": '',
                        "videoCodec": '',
                        "storageUri": '',
                        "contentType": '',
                        "productId": '',
                        "fileSizeByte": '',
                        "visibility": '',
                        "channelSurfingVisibility": '',
                        "epgVisibility": '',
                        "idx": '',
                        "status": '',
                        "index": 1,
                        "tripletStr": "8835.1.1030",
                        "title": "03 \u00d0 \u00d0\u017e\u00d0\u00a1\u00d0\u00a1\u00d0\u02dc\u00d0\u00af-2",
                        "uri": "tv:dvbt?trip=8835.1.1030&srvName=03%20%D0%A0%D0%9E%D0%A1%D0%A1%D0%98%D0%AF-2",
                        "dispNum": "002",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 2,
                        "tripletStr": "8835.1.1040",
                        "title": "04 \u00d0\u009d\u00d0\u00a2\u00d0\u2019",
                        "uri": "tv:dvbt?trip=8835.1.1040&srvName=04%20%D0%9D%D0%A2%D0%92",
                        "dispNum": "003",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 3,
                        "tripletStr": "8835.1.1050",
                        "title": "05 \u00d0\u0178\u00d0\u00af\u00d0\u00a2\u00d0\u00ab\u00d0\u2122 \u00d0\u0161\u00d0\u0090\u00d0\u009d\u00d0\u0090\u00d0\u203a",
                        "uri": "tv:dvbt?trip=8835.1.1050&srvName=05%20%D0%9F%D0%AF%D0%A2%D0%AB%D0%99%20%D0%9A%D0%90%D0%9D%D0%90%D0%9B",
                        "dispNum": "004",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 4,
                        "tripletStr": "8835.1.1060",
                        "title": "06 \u00d0 \u00d0\u017e\u00d0\u00a1\u00d0\u00a1\u00d0\u02dc\u00d0\u00af-\u00d0\u0161",
                        "uri": "tv:dvbt?trip=8835.1.1060&srvName=06%20%D0%A0%D0%9E%D0%A1%D0%A1%D0%98%D0%AF-%D0%9A",
                        "dispNum": "005",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 5,
                        "tripletStr": "8835.1.1080",
                        "title": "08 \u00d0\u0161\u00d0\u0090\u00d0 \u00d0\u00a3\u00d0\u00a1\u00d0\u2022\u00d0\u203a\u00d0\u00ac",
                        "uri": "tv:dvbt?trip=8835.1.1080&srvName=08%20%D0%9A%D0%90%D0%A0%D0%A3%D0%A1%D0%95%D0%9B%D0%AC",
                        "dispNum": "006",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 6,
                        "tripletStr": "8835.1.1090",
                        "title": "09 \u00d0\u017e\u00d0\u00a2\u00d0 ",
                        "uri": "tv:dvbt?trip=8835.1.1090&srvName=09%20%D0%9E%D0%A2%D0%A0",
                        "dispNum": "007",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 7,
                        "tripletStr": "8835.1.1100",
                        "title": "10 \u00d0\u00a2\u00d0\u2019 \u00d0\u00a6\u00d0\u00b5\u00d0\u00bd\u00d1\u201a\u00d1\u20ac",
                        "uri": "tv:dvbt?trip=8835.1.1100&srvName=10%20%D0%A2%D0%92%20%D0%A6%D0%B5%D0%BD%D1%82%D1%80",
                        "dispNum": "008",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 8,
                        "tripletStr": "8835.2.1020",
                        "title": "02 \u00d0 \u00d0\u017e\u00d0\u00a1\u00d0\u00a1\u00d0\u02dc\u00d0\u00af-1",
                        "uri": "tv:dvbt?trip=8835.2.1020&srvName=02%20%D0%A0%D0%9E%D0%A1%D0%A1%D0%98%D0%AF-1",
                        "dispNum": "009",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 9,
                        "tripletStr": "8835.3.1070",
                        "title": "07 \u00d0 \u00d0\u017e\u00d0\u00a1\u00d0\u00a1\u00d0\u02dc\u00d0\u00af-24",
                        "uri": "tv:dvbt?trip=8835.3.1070&srvName=07%20%D0%A0%D0%9E%D0%A1%D0%A1%D0%98%D0%AF-24",
                        "dispNum": "010",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 10,
                        "tripletStr": "8835.11.2010",
                        "title": "11 \u00d0 \u00d0\u2022\u00d0\u009d \u00d0\u00a2\u00d0\u2019",
                        "uri": "tv:dvbt?trip=8835.11.2010&srvName=11%20%D0%A0%D0%95%D0%9D%20%D0%A2%D0%92",
                        "dispNum": "011",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 11,
                        "tripletStr": "8835.11.2020",
                        "title": "12 \u00d0\u00a1\u00d0\u00bf\u00d0\u00b0\u00d1\u0081",
                        "uri": "tv:dvbt?trip=8835.11.2020&srvName=12%20%D0%A1%D0%BF%D0%B0%D1%81",
                        "dispNum": "012",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 12,
                        "tripletStr": "8835.11.2030",
                        "title": "13 \u00d0\u00a1\u00d0\u00a2\u00d0\u00a1",
                        "uri": "tv:dvbt?trip=8835.11.2030&srvName=13%20%D0%A1%D0%A2%D0%A1",
                        "dispNum": "013",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 13,
                        "tripletStr": "8835.11.2040",
                        "title": "14 \u00d0\u201d\u00d0\u00be\u00d0\u00bc\u00d0\u00b0\u00d1\u02c6\u00d0\u00bd\u00d0\u00b8\u00d0\u00b9",
                        "uri": "tv:dvbt?trip=8835.11.2040&srvName=14%20%D0%94%D0%BE%D0%BC%D0%B0%D1%88%D0%BD%D0%B8%D0%B9",
                        "dispNum": "014",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 14,
                        "tripletStr": "8835.11.2050",
                        "title": "15 \u00d0\u00a2\u00d0\u20193",
                        "uri": "tv:dvbt?trip=8835.11.2050&srvName=15%20%D0%A2%D0%923",
                        "dispNum": "015",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 15,
                        "tripletStr": "8835.11.2060",
                        "title": "16 \u00d0\u00a1\u00d0\u00bf\u00d0\u00be\u00d1\u20ac\u00d1\u201a \u00d0\u0178\u00d0\u00bb\u00d1\u017d\u00d1\u0081",
                        "uri": "tv:dvbt?trip=8835.11.2060&srvName=16%20%D0%A1%D0%BF%D0%BE%D1%80%D1%82%20%D0%9F%D0%BB%D1%8E%D1%81",
                        "dispNum": "016",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 16,
                        "tripletStr": "8835.11.2070",
                        "title": "17 \u00d0\u2014\u00d0\u00b2\u00d0\u00b5\u00d0\u00b7\u00d0\u00b4\u00d0\u00b0",
                        "uri": "tv:dvbt?trip=8835.11.2070&srvName=17%20%D0%97%D0%B2%D0%B5%D0%B7%D0%B4%D0%B0",
                        "dispNum": "017",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 17,
                        "tripletStr": "8835.11.2080",
                        "title": "18 \u00d0\u0153\u00d0\u02dc\u00d0 ",
                        "uri": "tv:dvbt?trip=8835.11.2080&srvName=18%20%D0%9C%D0%98%D0%A0",
                        "dispNum": "018",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 18,
                        "tripletStr": "8835.11.2090",
                        "title": "19 \u00d0\u00a2\u00d0\u009d\u00d0\u00a2",
                        "uri": "tv:dvbt?trip=8835.11.2090&srvName=19%20%D0%A2%D0%9D%D0%A2",
                        "dispNum": "019",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 19,
                        "tripletStr": "8835.11.2100",
                        "title": "20 \u00d0\u0153\u00d0\u00a3\u00d0\u2014 \u00d0\u00a2\u00d0\u2019",
                        "uri": "tv:dvbt?trip=8835.11.2100&srvName=20%20%D0%9C%D0%A3%D0%97%20%D0%A2%D0%92",
                        "dispNum": "020",
                        "programMediaType": "tv"
                    },
                    {
                        "index": 20,
                        "tripletStr": "8835.1.1110",
                        "title": "\u00d0\u2019\u00d0\u2022\u00d0\u00a1\u00d0\u00a2\u00d0\u02dc \u00d0\u00a4\u00d0\u0153",
                        "uri": "tv:dvbt?trip=8835.1.1110&srvName=%D0%92%D0%95%D0%A1%D0%A2%D0%98%20%D0%A4%D0%9C",
                        "dispNum": "500",
                        "programMediaType": "radio"
                    },
                    {
                        "index": 21,
                        "tripletStr": "8835.1.1120",
                        "title": "\u00d0\u0153\u00d0\u0090\u00d0\u00af\u00d0\u0161",
                        "uri": "tv:dvbt?trip=8835.1.1120&srvName=%D0%9C%D0%90%D0%AF%D0%9A",
                        "dispNum": "501",
                        "programMediaType": "radio"
                    },
                    {
                        "index": 22,
                        "tripletStr": "8835.1.1130",
                        "title": "\u00d0 \u00d0\u00b0\u00d0\u00b4\u00d0\u00b8\u00d0\u00be \u00d0 \u00d0\u00be\u00d1\u0081\u00d1\u0081\u00d0\u00b8\u00d0\u00b8",
                        "uri": "tv:dvbt?trip=8835.1.1130&srvName=%D0%A0%D0%B0%D0%B4%D0%B8%D0%BE%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8",
                        "dispNum": "502",
                        "programMediaType": "radio"
                    }
                ]
            ]
        },
        "getSourceList": {
            "params": [
                {
                    "scheme": "tv"
                }
            ],
            "result": [
                [
                    {
                        "source": "tv:dvbt"
                    },
                    {
                        "source": "extInput:composite"
                    },
                    {
                        "source": "extInput:hdmi"
                    },
                    {
                        "source": "extInput:scart"
                    },
                    {
                        "source": "extInput:widi"
                    }
                ]
            ]
        },
        "getSchemeList": {
            "params": [
                "1.0"
            ],
            "result": [
                [
                    {
                        "scheme": "extInput"
                    },
                    {
                        "scheme": "fav"
                    },
                    {
                        "scheme": "tv"
                    },
                    {
                        "scheme": "usb"
                    }
                ]
            ]
        },
        "setTvContentVisibility": {
            "params": [
                {
                    "channelSurfingVisibility": "",
                    "uri": "",
                    "visibility": "",
                    "epgVisibility": ""
                }
            ],
            "result": []
        },
        "setFavoriteContentList": {
            "params": [],
            "result": []
        },
        "deleteContent": {
            "params": [
                {
                    "uri": ""
                }
            ],
            "result": []
        },
        "getContentCount": {
            "params": [
                {
                    "source": "usb:recStorage",
                    "type": "",
                    "target": ""
                }
            ],
            "result": [
                {
                    "count": 23
                }
            ]
        }
    },
    "appControl": {
        "setTextForm": {
            "params": [],
            "result": []
        },
        "getTextForm": {
            "params": [],
            "result": []
        },
        "getApplicationStatusList": {
            "params": [
                "1.0"
            ],
            "result": [
                [
                    {
                        "status": "off",
                        "name": "textInput"
                    },
                    {
                        "status": "off",
                        "name": "webBrowse"
                    },
                    {
                        "status": "off",
                        "name": "cursorDisplay"
                    }
                ]
            ]
        },
        "setCsxUserAccount": {
            "params": [],
            "result": []
        },
        "getApplicationList": {
            "params": [
                "1.0"
            ],
            "result": [
                [
                    {
                        "title": "yagalooTV",
                        "uri": "kamaji://OPA-YAGALOOTV",
                        "icon": "http://portal.store.sonyentertainmentnetwork.com/haku/img/opera_apps/OPA-YAGALOOTV/168x168/OPA-YAGALOOTV.png"
                    },
                    {
                        "title": "Yallwire",
                        "uri": "kamaji://OPA-YALLWIRE",
                        "icon": "http://portal.store.sonyentertainmentnetwork.com/haku/img/opera_apps/OPA-YALLWIRE/168x168/OPA-YALLWIRE.png"
                    },
                    {
                        "title": "Yemek Tarifleri",
                        "uri": "kamaji://OPA-YEMEK-TARIFLERI",
                        "icon": "http://portal.store.sonyentertainmentnetwork.com/haku/img/opera_apps/OPA-YEMEK-TARIFLERI/168x168/OPA-YEMEK-TARIFLERI.png"
                    },
                    {
                        "title": "YogaSessions",
                        "uri": "kamaji://OPA-YOGASESSIONS",
                        "icon": "http://portal.store.sonyentertainmentnetwork.com/haku/img/opera_apps/OPA-YOGASESSIONS/168x168/OPA-YOGASESSIONS.png"
                    },
                    {
                        "title": "Young Hollywood",
                        "uri": "kamaji://OPA-YOUNG-HOLLYWOOD",
                        "icon": "http://portal.store.sonyentertainmentnetwork.com/haku/img/opera_apps/OPA-YOUNG-HOLLYWOOD/168x168/OPA-YOUNG-HOLLYWOOD.png"
                    },
                    {
                        "title": "Your kid TV",
                        "uri": "kamaji://OPA-YOUR-KID-TV",
                        "icon": "http://portal.store.sonyentertainmentnetwork.com/haku/img/opera_apps/OPA-YOUR-KID-TV/168x168/OPA-YOUR-KID-TV.png"
                    },
                    {
                        "title": "Zoomby",
                        "uri": "kamaji://OPA-ZOOMBY",
                        "icon": "http://portal.store.sonyentertainmentnetwork.com/haku/img/opera_apps/OPA-ZOOMBY/168x168/OPA-ZOOMBY.png"
                    },
                    {
                        "title": "zulki",
                        "uri": "kamaji://OPA-ZULKI",
                        "icon": "http://portal.store.sonyentertainmentnetwork.com/haku/img/opera_apps/OPA-ZULKI/168x168/OPA-ZULKI.png"
                    },
                    {
                        "title": "La Hague, la Nature \u00c3  l'\u00c3\u00a9tat brut!!!",
                        "uri": "kamaji://OPA-LA-HAGUE-LA-NATURE-A-LETAT-BRUT",
                        "icon": "http://portal.store.sonyentertainmentnetwork.com/haku/img/opera_apps/OPA-LA-HAGUE-LA-NATURE-A-LETAT-BRUT/168x168/OPA-LA-HAGUE-LA-NATURE-A-LETAT-BRUT.png"
                    },
                    {
                        "title": "Facebook",
                        "uri": "preset://facebook",
                        "icon": "http://192.168.1.2/sony/appControl/icon/pack%3AAppDataSource%2Fimg%2Fhome_AppFacebook.png"
                    },
                    {
                        "title": "TV Tweet",
                        "uri": "preset://twitter",
                        "icon": "http://192.168.1.2/sony/appControl/icon/pack%3AAppDataSource%2Fimg%2Fhome_AppTwitter.png"
                    },
                    {
                        "title": "Photo Share",
                        "uri": "preset://photoshare",
                        "icon": "http://192.168.1.2/sony/appControl/icon/pack%3AAppDataSource%2Fimg%2Fhome_AppPhotoshare.png"
                    },
                ]
            ]
        },
        "terminateApps": {
            "params": [
                "1.0"
            ],
            "result": []
        },
        "setActiveApp": {
            "params": [],
            "result": []
        }
    },
    "browser": {
        "setTextUrl": {
            "params": [],
            "result": []
        },
        "actBrowserControl": {
            "params": [],
            "result": []
        },
        "getBrowserBookmarkList": {
            "params": [
                "1.0"
            ],
            "result": [
                []
            ]
        },
        "getTextUrl": {
            "params": [],
            "result": [[]]
        }
    },
    "audio": {
        "getSpeakerSettings": {
            "params": [
                "1.0"
            ],
            "result": [
                {
                    "target": "tvPosition",
                    "currentValue": "table top"
                },
                {
                    "target": "subwooferLevel",
                    "currentValue": 5
                },
                {
                    "target": "subwooferFreq",
                    "currentValue": 80
                },
                {
                    "target": "subwooferPhase",
                    "currentValue": "normal"
                },
                {
                    "target": "subwooferPower",
                    "currentValue": "on"
                },
            ]
        },
        "setAudioVolume": {
            "params": [
                {
                    "volume": "2",
                    "target": "speaker"
                }
            ],
            "result": [
                0
            ]
        },
        "getVolumeInformation": {
            "params": [
                "1.0"
            ],
            "result": [
                [
                    {
                        "volume": 20,
                        "maxVolume": 100,
                        "minVolume": 0,
                        "target": "speaker",
                        "mute": False
                    },
                    {
                        "volume": 30,
                        "maxVolume": 100,
                        "minVolume": 0,
                        "target": "headphone",
                        "mute": False
                    }
                ]
            ]
        },
        "setAudioMute": {
            "params": [
                {
                    "status": False
                }
            ],
            "result": [
                0
            ]
        }
    },
    "cec": {
        "setMhlPowerFeedMode": {
            "params": [
                {
                    "enabled": True
                }
            ],
            "result": []
        },
        "setMhlAutoInputChangeMode": {
            "params": [
                {
                    "enabled": True
                }
            ],
            "result": []
        },
        "setCecControlMode": {
            "params": [
                {
                    "enabled": True
                }
            ],
            "result": []
        },
        "setPowerSyncMode": {
            "params": [
                {
                    "sourcePowerOnSync": True,
                    "sinkPowerOffSync": True
                }
            ],
            "result": []
        }
    }
}
