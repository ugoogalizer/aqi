#!/usr/bin/python
# -*- coding=utf-8 -*-
# "DATASHEET": http://cl.ly/ekot
# https://gist.github.com/kadamski/92653913a53baf9dd1a8
from __future__ import print_function
import serial, struct, sys, time, json, atexit
import logging
from os.path import exists

DEBUG = 0
CMD_MODE = 2
CMD_QUERY_DATA = 4
CMD_DEVICE_ID = 5
CMD_SLEEP = 6
CMD_FIRMWARE = 7
CMD_WORKING_PERIOD = 8
MODE_ACTIVE = 0
MODE_QUERY = 1

ser = serial.Serial()

sleep_sec = 60 #1 minute
stable_measurements = 15

# pi zero w
# ser.port = "/dev/ttyAMA0"
# ser.port = "/dev/ttyUSB0"
# json_path='/var/www/html/aqi.json'
# csv_path ='/var/www/html/aqi.csv'

# win debug
ser.port = "COM7"
json_path = '../html/aqi.json'
csv_path = "../html/aqi.csv"

ser.baudrate = 9600

ser.open()
ser.flushInput()

byte, data = 0, ""

def initiate_json(file_path):
    """
    Check to see if the aqi.json exists in the html directory and add it if not
    """
    if not exists(file_path):
        with open(file_path,"w") as fresh_file:
            fresh_file.write('[]')


def dump(d, prefix=''):
    print(prefix + ' '.join(x.encode('hex') for x in d))

def construct_command(cmd, data=[]):
    assert len(data) <= 12
    data += [0,]*(12-len(data))
    checksum = (sum(data)+cmd-2)%256
    ret = "\xaa\xb4" + chr(cmd)
    ret += ''.join(chr(x) for x in data)
    ret += "\xff\xff" + chr(checksum) + "\xab"

    if DEBUG:
        dump(ret, '> ')
    return ret

def process_data(d):
    r = struct.unpack('<HHxxBB', d[2:])
    pm25 = r[0]/10.0
    pm10 = r[1]/10.0
    checksum = sum(ord(v) for v in d[2:8])%256
    return [pm25, pm10]
    #print("PM 2.5: {} μg/m^3  PM 10: {} μg/m^3 CRC={}".format(pm25, pm10, "OK" if (checksum==r[2] and r[3]==0xab) else "NOK"))

def process_version(d):
    r = struct.unpack('<BBBHBB', d[3:])
    checksum = sum(ord(v) for v in d[2:8])%256
    print("Y: {}, M: {}, D: {}, ID: {}, CRC={}".format(r[0], r[1], r[2], hex(r[3]), "OK" if (checksum==r[4] and r[5]==0xab) else "NOK"))

def read_response():
    byte = 0
    while byte != "\xaa":
        byte = ser.read(size=1)

    d = ser.read(size=9)

    if DEBUG:
        dump(d, '< ')
    return byte + d

def cmd_set_mode(mode=MODE_QUERY):
    ser.write(construct_command(CMD_MODE, [0x1, mode]))
    read_response()

def cmd_query_data():
    ser.write(construct_command(CMD_QUERY_DATA))
    d = read_response()
    values = []
    if d[1] == "\xc0":
        values = process_data(d)
    return values

def cmd_set_sleep(sleep=1):
    mode = 0 if sleep else 1
    ser.write(construct_command(CMD_SLEEP, [0x1, mode]))
    read_response()

def cmd_set_working_period(period):
    ser.write(construct_command(CMD_WORKING_PERIOD, [0x1, period]))
    read_response()

def cmd_firmware_ver():
    ser.write(construct_command(CMD_FIRMWARE))
    d = read_response()
    process_version(d)

def cmd_set_id(id):
    id_h = (id>>8) % 256
    id_l = id % 256
    ser.write(construct_command(CMD_DEVICE_ID, [0]*10+[id_l, id_h]))
    read_response()


#function to disbale the sensor on exit

#function to clear the screen on exit
def cleanupOnExit():
    cmd_set_mode(0)
    cmd_set_sleep()
atexit.register(cleanupOnExit)

if __name__ == "__main__":
    #initiate_json()
    initiate_json(json_path)
    
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename='aqi.log', level=logging.DEBUG)
    logging.info('AQI Monitor has been started!')
    try:
        while True:
            logging.info('collection is starting')
            cmd_set_sleep(0)
            cmd_set_mode(1)
            print("Taking %s measurements to ensure a stable measurement" % str(stable_measurements))
            for t in range(stable_measurements):
                values = cmd_query_data()
                if values is not None and len(values)>0:
                    print("PM2.5: ", values[0], ", PM10: ", values[1])
                    logging.debug("values: PM2.5: {0}, PM10: {1}".format(values[0], values[1]))
                    time.sleep(2)
                else:
                    print("no reading, will retry")
                    time.sleep(5)
                    t -= 1

            if values is not None and len(values)>0:
                # open stored data
                logging.debug('Opening aqi.json')
                with open(json_path) as json_data:
                    data = json.load(json_data)

                # csv
                #logging.debug('Opening aqi.csv')
                #csv_file = open(csv_path, 'a')
                #csv_file.write("{0},{1},{2}\n".format(values[0],values[1],time.strftime("%d.%m.%Y %H:%M:%S")))
                #csv_file.close()
                #logging.debug('Closed aqi.csv')

                # check if length is more than 10000 and delete first element
                if len(data) > 10000:
                    data.pop(0)

                # append new values
                # data.append({'pm25': values[0], 'pm10': values[1], 'time': time.strftime("%d.%m.%Y %H:%M:%S")})
                # Using ctime() instead of strftime().  
                newdata = { 'time': time.ctime()}
                if len(values)>0:
                    newdata['pm25'] = values[0]
                    newdata['pm10'] = values[1]
                #data.append({'pm25': values[0], 'pm10': values[1], 'time': time.ctime()})
                data.append(newdata) #{'pm25': values[0], 'pm10': values[1], 'time': time.ctime()})

                # save it
                with open(json_path, 'w') as outfile:
                    json.dump(data, outfile)

            #print("Going to sleep for 5min...")
            print("Going to sleep for %s seconds..." % str(sleep_sec))
            #logging.info('sleeping for 5 minutes')
            logging.info('sleeping for %s seconds' % str(sleep_sec))
            cmd_set_mode(0)
            cmd_set_sleep()
            #time.sleep(300)
            time.sleep(sleep_sec)
    except KeyboardInterrupt:
        pass

