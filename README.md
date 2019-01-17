# softconsole_sensor_alert
This module was developed to adjust the screen brightness of the [kevinkahn's softconsole](https://github.com/kevinkahn/softconsole), but it could be used for many other sensors.
Some of the code borrowed from: https://github.com/ControlEverythingCommunity/TSL2561/blob/master/Python/TSL2561.py

Requires smbus, installed with:
```bash
$ sudo pip3 install smbus-cffi
$ sudo apt install -y i2c-tools  # need to verify this is needed
$ # And either on of the following:
$ 	sudo raspi-config # enable i2c interface
$ 	# enable i2c via /boot/config.txt and reboot
```

Here is a sample of what an alert config might look like:
```python
[Alerts]
        [[Dimmer]]
        Type = Periodic
        Interval = 5 seconds
        Invoke = SetDim.SensorOut
        Parameter = 5,10,15,15,40,60
```
Here are the parameters:
```python
alert.param[0] = DimLevel low/no light
alert.param[1] = DimLevel medium light
alert.param[2] = DimLevel high light
alert.param[3] = BrightLevel low/no light
alert.param[4] = BrightLevel medium light
alert.param[5] = DiBrightLevel high light
```
