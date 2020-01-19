#!/usr/bin/python
# -*- coding=utf-8 -*-
# "DATASHEET": http://cl.ly/ekot
# https://pypi.org/project/sds011/
# https://github.com/menschel/sds011
#from sds011 import SDS011
from sds011 import SDS011
import sys, time, json
import logging
import os
from os.path import exists
from datetime import datetime
from dateutil.tz import tzlocal

sleep_sec = 300 #frequency of measurements (60sec = 1 minute)
read_sec = 15 # how many seconds to read for
data_limit = 10000 # how many measurements to maintain in json


debug = 0       # debug level in sds011 class module
cycles = 4      # serial read timeout in seconds, dflt 2
timeout = 2     # timeout on serial line read
unit_of_measure = SDS011.UnitsOfMeasure.MassConcentrationEuropean
  
failure_tolerance = 5   # how many failed readings can we tolerate

baudrate = 9600

# pi zero w
port = "/dev/ttyUSB0"
json_path='/var/www/html/aqi.json'
csv_path ='/var/www/html/aqi.csv'

# win debug
#port = "COM7"
#json_path = '..\\html\\aqi.json'
#csv_path = "..\\html\\aqi.csv"


def printValues(timing, values, unit_of_measure):
    if unit_of_measure == SDS011.UnitsOfMeasure.MassConcentrationEuropean:
        unit = 'µg/m³'
    else:
        unit = 'pcs/0.01cft'
    print("Waited %d secs\nValues measured in %s:    PM2.5  " %
          (timing, unit), values[1], ", PM10 ", values[0])

def initiate_json(file_path):
    """
    Check to see if the aqi.json exists in the html directory and add it if not
    """
    if not exists(file_path) or os.stat(file_path).st_size == 0:
        with open(file_path,"w") as fresh_file:
            fresh_file.write('[]')

if __name__ == '__main__':

    #sensor = SDS011(port,baudrate=baudrate,use_query_mode=True)
    #sensor.sleep()
    print("Connecting to SDS011 and printing some stats:")
    
    # simple parsing the command arguments for setting options
    # Create an instance of your sensor
    # options defaults: logging None, debug level 0, serial line timeout 2
    # option unit_of_measure (default False) values in pcs/0.01sqf or mass ug/m3
    sensor = SDS011(port, timeout=timeout, unit_of_measure=unit_of_measure)

        
    # raise KeyboardInterrupt
    # Now we have some details about it
    print("SDS011 sensor info:")
    print("Device ID: ", sensor.device_id)
    print("Device firmware: ", sensor.firmware)
    print("Current device cycle (0 is permanent on): ", sensor.dutycycle)
    print(sensor.workstate)
    print(sensor.reportmode)


    # Set dutycyle to nocycle (permanent)
    sensor.reset()
    #Start off in Sleeping State 
    #sensor.workstate = SDS011.WorkStates.Sleeping

    #initiate_json()
    initiate_json(json_path)
    
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename='aqi.log', level=logging.DEBUG)
    logging.info('AQI Monitor has been started!')

    loop_forever = True
    
    try:
        while loop_forever:
            logging.info('Collection is starting')
            failures = 0

            # turn on diode and fans, get a reading
            print("Push sensor into wake state and waiting %s seconds" % read_sec)
            sensor.workstate = SDS011.WorkStates.Measuring
            
            # The sensor needs to warm up!
            time.sleep(read_sec)


            print("Taking measurement...")
            values = sensor.get_values()
            # create timestamp at time of measurements
            aqi_tsp = datetime.now(tzlocal()).isoformat() 

            #Sleep the sensor now we (should) have a measurement
            sensor.workstate = SDS011.WorkStates.Sleeping

            #Check for a valid measurement
            if values is not None and len(values)>0:

                # Create named variables
                newdata = { 'time': aqi_tsp} 
                newdata['pm25'] = values[1]
                newdata['pm10'] = values[0]

                print(aqi_tsp,", PM2.5: ", newdata['pm25'], ", PM10: ", newdata['pm10'])
                logging.debug("values: PM2.5: {0}, PM10: {1}".format(newdata['pm25'], newdata['pm10']))
                    
                # csv
                logging.debug('Opening aqi.csv')
                csv_file = open(csv_path, 'a')
                csv_file.write("{0},{1},{2}\n".format(newdata['pm25'],newdata['pm10'],aqi_tsp))
                csv_file.close()
                logging.debug('Closed aqi.csv')

                # open stored json data
                logging.debug('Opening aqi.json')
                with open(json_path) as json_data:
                    data = json.load(json_data)

                # check if length is more than data_limit and delete first element
                if len(data) > data_limit:
                    data.pop(0)

                # append new values
                data.append(newdata)

                # save it
                with open(json_path, 'w') as outfile:
                    json.dump(data, outfile)
            else:
                #Reading has failed, handle accordingly
                print("no reading, will retry")
              
                failures +=1 # update failure count
                if failures > failure_tolerance:
                    print("too many failures")
                    break
              

            print("Going to sleep for %s seconds..." % str(sleep_sec - read_sec))
            logging.info('sleeping for %s seconds' % str(sleep_sec - read_sec))

            #sensor.sleep() # turn off fan and diode
            time.sleep(sleep_sec - read_sec)

        # end of test
        print("\nSensor reset to normal")
        sensor.workstate = SDS011.WorkStates.Sleeping
        sensor = None


    except KeyboardInterrupt:
        print("Sensor reset due to a KeyboardInterrupt")
        loop_forever = False
        pass
    finally:
        print("turning off sensor, saving data")
        print("\nSensor reset to normal")
        sensor.workstate = SDS011.WorkStates.Sleeping
        sensor = None
        #sensor.sleep()
        #sds.sleep()
        # save json
        with open(json_path, 'w') as outfile:
            json.dump(data, outfile)
        