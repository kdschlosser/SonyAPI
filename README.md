## SonyAPI

Python connector for Sony Bravia generation 3 TV's.

This API I believe is one of if not these most complete API's outside of the Sony Partner circle. Sony was nice enough to only distribute API documentation to their partners. Which means that unless you have thousands of dollars to spend on a controller you are without the ability to externally control the TV.
Through a lot of research and some reverse engineering by myself and other developers is what made this connector possible. If there is something that I missed or is not functioning properly please submit an issue. If you have any questions on how it functions please submit an issue.


## The Basics
***Constructor:***

    instance = SonyAPI.SonyAPI(ip_address=None, pin=0000, psk=None, mac=None, ssdp_timeout=10)


If this is a first time connecting to the TV you can start the connector without passing a single thing to it. The API will go and retrieve a list of available TV's on your network and prompt you to select which TV you want to use. Once it has made the initial connected to the TV a box will appear on your TV screen prompting you to connect with a spicific pin. The API at the same time will ask for a pin. Enter that pin and also write it down for future connections. The pin entry has a 60 second timeout, if the timeout period expires the API will raise SonyAPI.RegisterTimeoutError.

Developer tidbit. If you want to intercept the prompts for the TV selection and the pin for something like a GUI you will want to override input()

If you have any issues with the automatic discovery you have several options. you cause pass the parameter ssdp_timeout with a higher value then 10 (seconds) or you can enter the IP address of the TV directly. If you enter the IP address you have to be sure you have your TV set to use a static IP address.
If you do not want to have the API prompt you for which TV you want to use you can once again use the IP address, or you can pass the mac address using the mac keyword. Use of the mac address is hinged on the TV being automatically discovered. if the discovery yields no TV's SonyAPI.IPAddressError will be raised.

Once you have completed the registration process the mac address as well as the pin that was entered can be pulled from the API so it can be written to a file or how ever you want to store the information.

    mac = instance.mac
    pin = instance.pin

You also can pass a personal access key instead of using the pairing this is handy in a multi TV system as you won't have to worry about keeping track of registrations and pin numbers. (if supported by the TV)

## Power

A couple of things about how the power works. With the Android based TV's they do have a power on command, and this command is tried first. if it does not suceed it will then check to see if wake on lan is enabled on the TV. If it is not it will enable the wake on lan then use that method to turn the TV on. There is no need to pass a mac address there is a mechanism in place that will acquire the mac address automatically.

***Power:***

  * Get

        state = instance.power

  * Set

        instance.power = True\False


## Volume

When changing the volume you will reference the device you want to control the volume for, This is found in the audio output settings of your TV.

***Volume:***
  * Get

        speaker_volume = int(instance.volume.speaker)
        headphone_volume = int(instance.volume.headphone)

  * Set

        instance.volume.speaker = 50
        instance.volume.headphone = 50

***Mute:***
  * Get

        speaker_mute = instance.volume.speaker.mute
        headphone_mute = instance.volume.headphone.mute

  * Set

        instance.volume.speaker.mute = True/False
        instance.volume.headphone.mute = True/False

***Minimum Volume:***

  * Get

        min_speaker = instance.volume.speaker.min_volume
        min_headphone = instance.volume.headphone.min_volume
***Maximum Volume:***

  * Get

        max_speaker = instance.volume.speaker.max_volume
        max_headphone = instance.volume.headphone.max_volume

***Volume Up:***

    instance.volume.speaker.up()
    instance.volume.headphone.up()


***Volume Down:***

    instance.volume.speaker.down()
    instance.volume.headphone.down()


 I have also set this up to allow for the use of some of the rich comparison and augmented arithmetic operators += -= *= /= > < == >= <= !=

    instance.volume.speaker += 1
    instance.volume.headphone += 1

    instance.volume.speaker -= 1
    instance.volume.headphone -= 1
## Channels

Channels work the same way the volume does but without the speaker or headphone.

    instance.channel.up()
    instance.channel.down()
    instance.channel += 1
    instance.channel = 15
    channel = int(instance.channel)

There is also the property lineup which will return a list of ContentItem instances.

    channel_lineup = instance.channel.lineup

## Content

There are 2 different types of content. the first one being a media.NowPlaying object and the second one being a media.ContentItem.
The ContentItem object is going to be found in a list of available content gotten by using

    instance.channel.lineup
    InputItem.content

The ContentItem is a container for all kinds of metadata as well as some methods to perform different tasks

***The available attributes/properties are:***

  * index
  * triplet_str
  * title
  * direct_remote_num
  * is_protected
  * is_already_played
  * uri
  * program_num
  * display_num
  * original_display_num
  * program_media_type
  * channel_name
  * source
  * user_content_flag
  * created_time
  * size_mb
  * parental_country
  * parental_system
  * parental_rating
  * subtitle_title
  * subtitle_language
  * audio_channel
  * audio_frequency
  * audio_codec
  * chapter_count
  * video_codec
  * storage_uri
  * content_type
  * product_id
  * file_size_byte
  * visibility
  * channel_surfing_visibility
  * epg_visibility
  * idx
  * status
  * duration
  * start_time
  * remaining
  * elapsed
  * percent_elapsed
  * end_time

***Available methods are:***
  * set()
  * delete()
  * remove_recording_schedule()
  * add_recording_schedule(quality, repeat_type)
  * delete_protection(enable=bool)
  * tv_content_visibility(visibility=None, surfing_visibility=None, epg_visibility=None)







