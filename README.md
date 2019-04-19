# aqi
Measure AQI based on PM2.5 or PM10 with a Raspberry Pi and a SDS011 particle sensor.

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
