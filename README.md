SonyAPI

This is the initial release of a python connector to Sony generation 3 TV's.

The API is pretty simple. This API will automatically get the MAC address of the TV to create the WOL packet  so you will be able to wake it from standby. It also automatically will get the FQDN of the computer running this lib and grab the mac adress from the network card and use that information to create a client id and nickname. This is done so the use of the same pin and hostname cannot be used to access the TV. This adds a little bit of extra security.

constructor

    instance = SonyAPI(ip_address)

connector, use 0000 if it is a new registration. will return True/False/None True if the connection succeeded False if the connection failed and None if it is in registration mode. when in registration mode if the registration is not completed within 60 seconds by calling connect again with the pin entered that the TV generates the exception SonyApi.RegisterTimeoutError will be raised. If you have unregistered the device form the TV and the connector tries to connect with an invalid pi the exception SonyAPI.PinError will be raised.

    instance.connect(pin)

When changing the volume you will reference the device you want to control the volume for, This is found in the audio output settings of your TV.

gets the volume

    volume = instance.speakers.volume
    
sets the volume
    
    instance.speakers.volume = 50
    
gets the mute state

    mute = instance.speakers.mute
    
sets the mute state

    instance.speakers.mute = True/False
    
gets the minimum volume    

    min_volume = instance.speakers.min_volume
    
gets the maximum volume

    max_folume = instance.speakers.max_volume

