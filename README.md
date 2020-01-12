# aqi-pi
Measure AQI based on PM2.5 or PM10 with a Raspberry Pi and a SDS011 particle sensor.  In my case I used the Raspberry Pi Zero W.
This package also  displays AQI information on a Adafruit 128x32 Mini OLED device () attached to the Pi. This allows the device to become portable when run from a portable USB power supply and not require WiFi or access to a web browser to see the results.

Original inspiration from Hackernoon's https://hackernoon.com/how-to-measure-particulate-matter-with-a-raspberry-pi-75faa470ec35 and the corresponding github: https://github.com/zefanja/aqi

Working
* HTTP webpage displaying current sensor measu
* OLED Display (intended to display aqi result on local display to enable portable measurements)
* RESTful API (intended to access from Home Assistant (homeassistant.io))

Not Working and on the TODO list: 
* Sensor of PM10 and PM2.5 measurements (waiting postal service of sensor itself)
* Home Assistant yaml configuration to read from RESTful interface
* HTTP webpage (plot.ly) displaying historic sensor measurements
* Migrate sensor code from Python2 to Python3
* Run code in python virtual environment
* Tidy up repo removing unused artifacts
* Publish to a public location, current plan is to http://sensor.community (also known as https://luftdaten.info/)



## Pre-Requisitites

* Install raspbian on the pi.
* Clone this (or a forked copy) of this repo to your pi: 
```
 git clone https://github.com/ugoogalizer/aqi-pi.git
```
* Copy the contents of the html directory into /var/www/html
```
sudo cp ./html/* /var/www/html
sudo apt install python-serial python-enum lighttpd
```

## OLED Display Setup

Don't plug in the OLED display to your pi yet...

### Install Python Libs
On the raspberry pi (as per https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage)
```
sudo apt-get install python3-pip
sudo pip3 install adafruit-circuitpython-ssd1306
sudo apt-get install python3-pil
```

### Enable I2C and Serial Port on Raspberry Pi
As per: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

Use raspi-config to enable I2C Interface and install required (testing?) software

```
sudo apt-get install -y python-smbus i2c-tools
sudo raspi-config
<make changes>
<also enable the serial interface while there (but don't enable login shell)>
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

## Run Everything

### Run the Sensor

On the raspberry pi from the local copy of the git repo, run: 

```
sudo python2 ./python/aqi.py
```

### Run the display stats script: 

On the raspberry pi from the local copy of the git repo, run: 
```
sudo python3 ./python/display.py
```
CTRL+C quits the display (and now turns off the display rather than leaves it to run and burn out your screen)

## Creating the RESTful Interface

Run a simple RESTful interface using Python3 and Flask that returns the latest sensor status in JSON format, intended for ingestion into Home Assistant (https://www.home-assistant.io/integrations/rest/) but could be ingested by other sources.


```
sudo pip3 install flask
sudo python3 ./python/restful_api.py
```

API is available at: http://0.0.0.0:81/aqi/v1.0/aqi and returns JSON: 
```
{
  "Overall AQI": 1,
  "Overall AQI band": "low",
  "PM10 AQI": 1,
  "PM2.5 AQI": 1,
  "pm10": 70.0,
  "pm25": 301.5,
  "time": "08.01.2020 22:04:05"
}
```

Inspiration from this came from: https://auth0.com/blog/developing-restful-apis-with-python-and-flask/ and http://mattrichardson.com/Raspberry-Pi-Flask/


## Optional Steps

If you don't have a sensor yet and want to test without it, you can use the example data in the git repo by: 
```
sudo cp /var/www/html/api-example.json /var/www/html/aqi.json
```
