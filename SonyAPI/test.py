import traceback

try:
    Error = __import__('__builtin__.Exception')
except ImportError:
    Error = __import__('builtins.Exception')

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


def run(sony_api):
    print(sony_api.discover())

    def p(*attr_name):
        if len(attr_name) == 1:
            attr_name = attr_name[0]

            if attr_name.endswith(':'):
                print(attr_name)

            else:
                try:
                    print(attr_name + ':', repr(getattr(sony_api, attr_name)))
                except Error:
                    print(attr_name + ':', traceback.format_exc())
        else:
            label, attrs = attr_name
            found_names = []

            for attr in attrs:
                if found_names:
                    for attr_name in found_names:
                        print(
                            '    %s.%s: %r' %
                            (label, attr_name, getattr(attr, attr_name))
                        )
                else:
                    for attr_name in ATTR_NAMES:
                        try:
                            if hasattr(attr, attr_name):
                                found_names += [attr_name]
                                print(
                                    '    %s.%s: %r' %
                                    (
                                        label,
                                        attr_name,
                                        getattr(attr, attr_name)
                                    )
                                )
                        except Error:
                            print(
                                '    %s.%s: %s' %
                                (label, attr_name, traceback.format_exc())
                            )

    print('============================================================')
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

    print('============================================================')
    print('mute:')
    print('    mute:', speaker.mute)
    speaker.mute = True
    print('    mute:', speaker.mute)
    speaker.mute = False
    print('    mute:', speaker.mute)

    print('============================================================')
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

    print('============================================================')
    p('time_format')
    p('date_format')
    p('time')
    p('postal_code')
    p('power_saving_mode')
    p('interface_server_name')
    p('interface_model_name')
    p('interface_product_name')
    p('interface_product_category')
    p('interface_version')
    p('remote_model')
    p('product')
    p('mac')
    p('name')
    p('language')
    p('cid')
    p('generation')
    p('model')
    p('serial')
    p('wol_mode')
    p('color_keys_layout')
    p('led_indicator_status')
    p('remote_device_settings')
    p('network_ipv4')
    p('network_netif')
    p('network_ipv6')
    p('network_subnet_mask')
    p('network_dns')
    p('network_mac')
    p('network_gateway')
    p('wol_mac')
    p('chinese_software_keyboard_supported')
    p('pip_sub_screen_position')
    p('audio_source_screen')
    p('multi_screen_mode')
    p('multi_screen_internet_mode')
    p('parental_rating_setting_country')
    p('parental_rating_setting_unrated')
    p('parental_rating_setting_age')
    p('parental_rating_setting_sony')
    p('parental_rating_setting_tv')
    p('parental_rating_setting_mpaa')
    p('parental_rating_setting_french')
    p('parental_rating_setting_english')
    p('browser_text_url')
    p('recording_status')
    p('recording_supported_repeat_type')
    p('command_list')
    print('============================================================')

    print('scheme_list:')
    for item in sony_api.scheme_list:
        print('    scheme:', repr(item))
    print('============================================================')

    print('application_status_list:')
    for item in sony_api.application_status_list:
        print('    name, status:', item)
    print('============================================================')

    print('content_count:')
    for item in sony_api.content_count:
        print('    inputs.InputItem, count:', item)
    print('============================================================')

    print('browser_bookmark_list:')
    p('browser.BookmarkItem', sony_api.browser_bookmark_list)

    print('source_list:')
    p('inputs.InputItem', sony_api.source_list)

    print('application_list:')
    p('application.Application', sony_api.application_list)

    print('recording_history_list:')
    p('recording.HistoryItem', sony_api.recording_history_list)

    print('recording_schedule_list:')
    p('recording.ScheduleItem', sony_api.recording_schedule_list)

    print('recording_conflict_list:')
    p('recording.ScheduleItem:', sony_api.recording_conflict_list)

    print('content_list:')
    p('media.ContentItem', sony_api.content_list)

    print('now_playing:')
    p('media.NowPlaying', sony_api.now_playing)
