# aqi-pi
Measure AQI based on PM2.5 or PM10 with a Raspberry Pi and a SDS011 particle sensor.  In my case I used the Raspberry Pi Zero W.
Intended to also display API information Adafruit 128x32 Mini OLED device ()

Original inspiration from Hackenoon's https://hackernoon.com/how-to-measure-particulate-matter-with-a-raspberry-pi-75faa470ec35 and the corresponding github: https://github.com/zefanja/aqi

Working
* Nothing yet...

Not Working: 
* Sensor of PM10 and PM2.5
* HTTP webpage displaying current sensor measurements
* HTTP webpage (plot.ly) displaying historic sensor measurements
* RESTful API (intended to access from Home Assistant (homeassistant.io))
* OLED Disply (intended to display aqi result on local display to enable portable measurements)


## Pre-Requisitites

* Install raspbian on the pi.
* Clone this (or a forked copy) of this repo to your pi: 
```
 git clone https://github.com/ugoogalizer/aqi-pi.git
```



## Setup OLED Display

Don't plug in the OLED display to your pi yet...

### Install Python Libs
On the raspberry pi (as per https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage)
```
sudo apt-get install python3-pip
sudo pip3 install adafruit-circuitpython-ssd1306
sudo apt-get install python3-pil
```

### Enable I2C
As per: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

Use raspi-config to enable I2C Interface and install required (testing?) software

```
sudo apt-get install -y python-smbus i2c-tools
sudo raspi-config
<make changes>
sudo shutdown -h now
```

Now you can plug in the OLED to the display, then power it back on.

### Test I2C

Run: 
```
sudo  i2cdetect -y 1
```
You should see something like: 
![I2C result screen](https://cdn-learn.adafruit.com/assets/assets/000/074/057/medium800/adafruit_products_i2c.png?1554480832)

## Installation
Currently, this package only works in `python2` due to its use of strings as bytestrings. As a result, from the 
repository root, run
```bash
sudo apt install python-serial python-enum lighttpd
virtualenv venv
. venv/bin/activate
pip install -e .
```

## Usage
```bash
python2 sensor.py
```

## Example output
```
{'PM2.5': 3.3, 'PM10': 6.2, 'time': '20.04.2019 17:03:42', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.3, 'PM10': 6.3, 'time': '20.04.2019 17:03:43', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.4, 'PM10': 6.6, 'time': '20.04.2019 17:03:44', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.4, 'PM10': 6.6, 'time': '20.04.2019 17:03:45', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.5, 'PM10': 6.9, 'time': '20.04.2019 17:03:46', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.5, 'PM10': 6.8, 'time': '20.04.2019 17:03:47', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.5, 'PM10': 7.1, 'time': '20.04.2019 17:03:48', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.5, 'PM10': 7.1, 'time': '20.04.2019 17:03:49', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.5, 'PM10': 7.0, 'time': '20.04.2019 17:03:50', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.5, 'PM10': 6.8, 'time': '20.04.2019 17:03:52', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.5, 'PM10': 6.8, 'time': '20.04.2019 17:03:53', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.5, 'PM10': 6.7, 'time': '20.04.2019 17:03:54', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.4, 'PM10': 6.6, 'time': '20.04.2019 17:03:55', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.4, 'PM10': 6.5, 'time': '20.04.2019 17:03:56', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.4, 'PM10': 6.4, 'time': '20.04.2019 17:03:57', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.4, 'PM10': 6.3, 'time': '20.04.2019 17:03:58', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.4, 'PM10': 6.4, 'time': '20.04.2019 17:03:59', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.3, 'PM10': 6.3, 'time': '20.04.2019 17:04:00', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.4, 'PM10': 6.6, 'time': '20.04.2019 17:04:01', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.4, 'PM10': 6.9, 'time': '20.04.2019 17:04:03', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.5, 'PM10': 7.0, 'time': '20.04.2019 17:04:04', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
{'PM2.5': 3.5, 'PM10': 7.0, 'time': '20.04.2019 17:04:05', 'PM10 AQI': 1, 'Overall AQI band': 'low', 'Overall AQI': 1, 'PM2.5 AQI': 1}
```
