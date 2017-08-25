## SonyAPI

This is the initial release of a python connector to Sony generation 3 TV's.

The API is pretty simple. This API will automatically get the MAC address of the TV to create the WOL packet  so you will be able to wake it from standby. It also automatically will get the FQDN of the computer running this lib and grab the mac adress from the network card and use that information to create a client id and nickname. This is done so the use of the same pin and hostname cannot be used to access the TV. This adds a little bit of extra security.

***Constructor:***

    instance = SonyAPI(ip_address, pin=0000, psk=None, debug=None)

The constructor can be passed a pin number if you want to pair the TV to the API or it can be passed a personal access key which can also be set up on the TV.

If you do not have the TV paired you will need to pass 0000 for the pin number or simply do not specify one. If the TV requires pairing and you have initialized the constructor you will be prompted to enter the pin number and this will time out in 60 seconds and generate a SonyAPI.RegisterError exception.

I used rawinput to allow entry for the pin number and this can be overridden very easily if you are wanting to use a GUI control to allow entry for the pin number.

## Power

A couple of things about how the power works. With the Android based TV's they do have a power on command, and this command is tried first. if it does not suceed it will then check to see if wake on lan is enabled on the TV. If it is not it will enable the wake on lan then use that method to turn the TV on. There is no need to pass a mac address there is a mechanism in place that will acquire the mac address automatically.

***Power:***

  * Get

        state = instance.power

  * Set

        instance.power = True\False


## Volume

When changing the volume you will reference the device you want to control the volume for, This is found in the audio output settings of your TV.

***Volume***
  * Get

        volume = instance.speakers.volume

  * Set

        instance.speakers.volume = 50

***Mute***
  * Get

        mute = instance.speakers.mute

  * Set

        instance.speakers.mute = True/False

***Minimum Volume***

  * Get

        min_volume = instance.speakers.min_volume

***Maximum Volume***

  * Get

        max_volume = instance.speakers.max_volume


## Channels

***Channel***

  * Get

      channel = instance.channel

  * Set

      instance.channel = 2

***Channel Up***

    instance.ChannelUp()


***Channel Down***

    instance.ChannelDown()





