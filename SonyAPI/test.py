import traceback


def run(sony_api):
    def Print(attr_name):
        try: print attr_name + ':', repr(getattr(sony_api, attr_name))
        except: print attr_name + ':', traceback.format_exc()

    print '============================================================'
    print 'volume:'
    speaker = sony_api.volume.speaker
    print '    volume:', speaker, '%'
    speaker.up()
    print '    volume:', speaker, '%'
    speaker.down()
    print '    volume:', speaker, '%'
    speaker += 1
    print '    volume:', speaker, '%'
    speaker -= 1
    print '    volume:', speaker, '%'

    print '============================================================'
    print 'mute:'
    print '    mute:', speaker.mute
    speaker.mute = True
    print '    mute:', speaker.mute
    speaker.mute = False
    print '    mute:', speaker.mute

    print '============================================================'
    print 'channel:'
    channel = sony_api.channel

    try:
        print '    channel:', channel
        speaker.up()
        print '    channel:', channel
    except:
        print '    channel:', traceback.format_exc()
    try:
        speaker.down()
        print '    channel:', channel
    except:
        print '    channel:', traceback.format_exc()

    try:
        speaker += 1
        print '    channel:', channel
    except:
        print '    channel:', traceback.format_exc()
    try:
        speaker -= 1
        print '    channel:', channel
    except:
        print '    channel:', traceback.format_exc()

    print '============================================================'
    Print('time_format')
    Print('date_format')
    Print('time')
    Print('postal_code')
    Print('power_saving_mode')
    Print('interface_server_name')
    Print('interface_model_name')
    Print('interface_product_name')
    Print('interface_product_category')
    Print('interface_version')
    Print('remote_model')
    Print('product')
    Print('mac')
    Print('name')
    Print('language')
    Print('cid')
    Print('generation')
    Print('model')
    Print('serial')
    Print('wol_mode')
    Print('color_keys_layout')
    Print('led_indicator_status')
    Print('remote_device_settings')
    Print('network_ipv4')
    Print('network_netif')
    Print('network_ipv6')
    Print('network_subnet_mask')
    Print('network_dns')
    Print('network_mac')
    Print('network_gateway')
    Print('wol_mac')
    Print('chinese_software_keyboard_supported')
    Print('pip_sub_screen_position')
    Print('audio_source_screen')
    Print('multi_screen_mode')
    Print('multi_screen_internet_mode')
    Print('parental_rating_setting_country')
    Print('parental_rating_setting_unrated')
    Print('parental_rating_setting_age')
    Print('parental_rating_setting_sony')
    Print('parental_rating_setting_tv')
    Print('parental_rating_setting_mpaa')
    Print('parental_rating_setting_french')
    Print('parental_rating_setting_english')
    Print('browser_text_url')
    Print('browser_bookmark_list')
    Print('recording_status')
    Print('recording_supported_repeat_type')
    Print('command_list')

    print '============================================================'
    content = sony_api.playing_content
    print 'playing_content:'
    print '    media.NowPlaying.program_title:', repr(content.program_title)
    print '    media.NowPlaying.triplet_str:', repr(content.triplet_str)
    print '    media.NowPlaying.title:', repr(content.title)
    print '    media.NowPlaying.bivl_provider:', repr(content.bivl_provider)
    print '    media.NowPlaying.uri:', repr(content.uri)
    print '    media.NowPlaying.program_num:', repr(content.program_num)
    print '    media.NowPlaying.media_type:', repr(content.media_type)
    print '    media.NowPlaying.source:', repr(content.source)
    print '    media.NowPlaying.display_num:', repr(content.display_num)
    print '    media.NowPlaying.original_display_num:', repr(content.original_display_num)
    print '    media.NowPlaying.bivl_asset_id:', repr(content.bivl_asset_id)
    print '    media.NowPlaying.bivl_service_id:', repr(content.bivl_service_id)
    print '    media.NowPlaying.play_speed:', repr(content.play_speed)

    try: print '    media.NowPlaying.start_time:', repr(content.start_time)
    except: print '    media.NowPlaying.start_time:', traceback.format_exc()
    try: print '    media.NowPlaying.remaining:', repr(content.remaining)
    except: print '    media.NowPlaying.remaining:', traceback.format_exc()
    try: print '    media.NowPlaying.elapsed:', repr(content.elapsed)
    except: print '    media.NowPlaying.elapsed:', traceback.format_exc()
    try: print '    media.NowPlaying.percent_elapsed:', repr(content.percent_elapsed)
    except: print '    media.NowPlaying.percent_elapsed:', traceback.format_exc()
    try: print '    media.NowPlaying.end_time:', repr(content.end_time)
    except: print '    media.NowPlaying.end_time:', traceback.format_exc()

    print '============================================================'
    print 'scheme_list:'
    for item in sony_api.scheme_list:
        print '    scheme:', repr(item)
    print '============================================================'

    print 'source_list:'
    for item in sony_api.source_list:
        print '    inputs.InputItem.title:', repr(item.title)
        print '    inputs.InputItem.connection:', repr(item.connection)
        print '    inputs.InputItem.uri:', repr(item.uri)
        print '    inputs.InputItem.label:', repr(item.label)
        print '    inputs.InputItem.icon:', repr(item.icon)
        print '------------------------------------------------------------'

    print '============================================================'
    inputs = sony_api.external_input_status
    print 'external_input_status:'

    for inpt in inputs:
        print '    inputs.InputItem.title:', repr(inpt.title)
        print '    inputs.InputItem.connection:', repr(inpt.connection)
        print '    inputs.InputItem.uri:', repr(inpt.uri)
        print '    inputs.InputItem.label:', repr(inpt.label)
        print '    inputs.InputItem.icon:', repr(inpt.icon)
        print '------------------------------------------------------------'

    print '============================================================'
    print 'content_count:'
    for item in sony_api.content_count:
        print '    inputs.InputItem, count:', item

    print '============================================================'
    print 'application_status_list:'
    for item in sony_api.application_status_list:
        print '    name, status:', item

    print '============================================================'
    print 'application_list:'
    for item in sony_api.application_list:
        print '    application.Application.title:', repr(item.title)
        print '    application.Application.data:', repr(item.data)
        print '    application.Application.uri:', repr(item.uri)
        print '    application.Application.display_icon:', repr(item.display_icon)
        print '    application.Application.icon:', repr(item.icon)
        print '------------------------------------------------------------'

    print '============================================================'
    items = sony_api.recording_history_list
    print 'recording_history_list:'
    for item in items:
        print '    recording.HistoryItem.title:', repr(item.title)
        print '    recording.HistoryItem.reason_msg:', repr(item.reason_msg)
        print '    recording.HistoryItem.reason_id:', repr(item.reason_id)
        print '    recording.HistoryItem.channel_name:', repr(item.channel_name)
        print '    recording.HistoryItem.id:', repr(item.id)
        try: print '    recording.HistoryItem.start_time:', repr(item.start_time)
        except: print '    recording.HistoryItem.start_time:', traceback.format_exc()
        try: print '    recording.HistoryItem.remaining:', repr(item.remaining)
        except: print '    recording.HistoryItem.remaining:', traceback.format_exc()
        try: print '    recording.HistoryItem.elapsed:', repr(item.elapsed)
        except: print '    recording.HistoryItem.elapsed:', traceback.format_exc()
        try: print '    recording.HistoryItem.percent_elapsed:', repr(item.percent_elapsed)
        except: print '    recording.HistoryItem.percent_elapsed:', traceback.format_exc()
        try: print '    recording.HistoryItem.end_time:', repr(item.end_time)
        except: print '    recording.HistoryItem.end_time:', traceback.format_exc()
        print '------------------------------------------------------------'

    print '============================================================'
    items = sony_api.recording_schedule_list
    print 'recording_schedule_list:'
    for item in items:
        print '    recording.ScheduleItem.recording_status:', repr(item.recording_status)
        print '    recording.ScheduleItem.title:', repr(item.title)
        print '    recording.ScheduleItem.quality:', repr(item.quality)
        print '    recording.ScheduleItem.uri:', repr(item.uri)
        print '    recording.ScheduleItem.overlap_status:', repr(item.overlap_status)
        print '    recording.ScheduleItem.repeat_type:', repr(item.repeat_type)
        print '    recording.ScheduleItem.channel_name:', repr(item.channel_name)
        print '    recording.ScheduleItem.type:', repr(item.type)
        print '    recording.ScheduleItem.id:', repr(item.id)
        try: print '    recording.ScheduleItem.start_time:', repr(item.start_time)
        except: print '    recording.ScheduleItem.start_time:', traceback.format_exc()
        try: print '    recording.ScheduleItem.remaining:', repr(item.remaining)
        except: print '    recording.ScheduleItem.remaining:', traceback.format_exc()
        try: print '    recording.ScheduleItem.elapsed:', repr(item.elapsed)
        except: print '    recording.ScheduleItem.elapsed:', traceback.format_exc()
        try: print '    recording.ScheduleItem.percent_elapsed:', repr(item.percent_elapsed)
        except: print '    recording.ScheduleItem.percent_elapsed:', traceback.format_exc()
        try: print '    recording.ScheduleItem.end_time:', repr(item.end_time)
        except: print '    recording.ScheduleItem.end_time:', traceback.format_exc()
        print '------------------------------------------------------------'

    print '============================================================'
    print 'recording_conflict_list:'
    items = sony_api.recording_conflict_list
    for item in items:
        print '    recording.ScheduleItem:', item

    print '============================================================'
    items = sony_api.content_list
    print 'content_list:'
    for item in items:
        print '    media.ContentItem.title:', repr(item.title)
        print '    media.ContentItem.uri:', repr(item.uri)
        print '    media.ContentItem.index:', repr(item.index)
        print '    media.ContentItem.triplet_str:', repr(item.triplet_str)
        print '    media.ContentItem.direct_remote_num:', repr(item.direct_remote_num)
        print '    media.ContentItem.is_protected:', repr(item.is_protected)
        print '    media.ContentItem.is_already_played:', repr(item.is_already_played)
        print '    media.ContentItem.program_num:', repr(item.program_num)
        print '    media.ContentItem.display_num:', repr(item.display_num)
        print '    media.ContentItem.original_display_num:', repr(item.original_display_num)
        print '    media.ContentItem.program_media_type:', repr(item.program_media_type)
        print '    media.ContentItem.source:', repr(item.source)
        try: print '    media.ContentItem.start_time:', repr(item.start_time)
        except: print '    media.ContentItem.start_time:', traceback.format_exc()
        try: print '    media.ContentItem.remaining:', repr(item.remaining)
        except: print '    media.ContentItem.remaining:', traceback.format_exc()
        try: print '    media.ContentItem.elapsed:', repr(item.elapsed)
        except: print '    media.ContentItem.elapsed:', traceback.format_exc()
        try: print '    media.ContentItem.percent_elapsed:', repr(item.percent_elapsed)
        except: print '    media.ContentItem.percent_elapsed:', traceback.format_exc()
        try: print '    media.ContentItem.end_time:', repr(item.end_time)
        except: print '    media.ContentItem.end_time:', traceback.format_exc()
        print '------------------------------------------------------------'
