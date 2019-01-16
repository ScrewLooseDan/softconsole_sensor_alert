# softconsole_sensor_alert
This module was developed to adjust the screen brightness of the [kevinkahn's softconsole](https://github.com/kevinkahn/softconsole), but it could be used for many other sensors.

Requires smbus, installed with:
- sudo pip3 install smbus-cffi
- sudo apt install -y i2c-tools  # need to verify this is needed
- And either on of the following:
	- sudo raspi-config # enable i2c interface
	- enable i2c via /boot/config.txt and reboot

