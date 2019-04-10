#!/usr/bin/python
# coding=utf-8
from __future__ import print_function
import json
import serial
import struct
import time


DEBUG = 0
CMD_MODE = 2
CMD_QUERY_DATA = 4
CMD_DEVICE_ID = 5
CMD_SLEEP = 6
CMD_FIRMWARE = 7
CMD_WORKING_PERIOD = 8
MODE_ACTIVE = 0
MODE_QUERY = 1


serial_interface = serial.Serial()
serial_interface.port = '/dev/ttyUSB0'
serial_interface.baudrate = 9600

serial_interface.open()
serial_interface.flushInput()

data = ''


def dump(data, prefix=''):
    print(prefix + ' '.join(x.encode('hex') for x in data))


def construct_command(command, data=None):
    data = data or []
    assert len(data) <= 12
    data += [0] * (12 - len(data))
    checksum = (sum(data) + command - 2) % 256
    ret = '\xaa\xb4' + chr(command)
    ret += ''.join(chr(x) for x in data)
    ret += '\xff\xff' + chr(checksum) + '\xab'

    if DEBUG:
        dump(ret, '> ')
    return ret


def process_data(data):
    r = struct.unpack('<HHxxBB', data[2:])
    pm25 = r[0] / 10.0
    pm10 = r[1] / 10.0
    checksum = sum(ord(v) for v in data[2:8]) % 256
    return {'time': time.strftime('%d.%m.%Y %H:%M:%S'), 'PM2.5': pm25, 'PM10': pm10}
    #print('PM 2.5: {} μg/m^3  PM 10: {} μg/m^3 CRC={}'.format(pm25, pm10, 'OK' if (checksum==r[2] and r[3]==0xab) else 'NOK'))


def process_version(d):
    r = struct.unpack('<BBBHBB', d[3:])
    checksum = sum(ord(v) for v in d[2:8]) % 256
    print(
        'Y: {}, M: {}, D: {}, ID: {}, CRC={}'
        .format(r[0], r[1], r[2], hex(r[3]), 'OK' if (checksum == r[4] and r[5] == 0xab) else 'NOK')
    )


def read_response():
    byte = 0

    while byte != '\xaa':
        byte = serial_interface.read(size=1)

    data = serial_interface.read(size=9)

    if DEBUG:
        dump(data, '< ')

    return byte + data


def cmd_set_mode(mode=MODE_QUERY):
    serial_interface.write(construct_command(CMD_MODE, [0x1, mode]))
    read_response()


def cmd_query_data():
    serial_interface.write(construct_command(CMD_QUERY_DATA))
    d = read_response()


    if d[1] == '\xc0':
        return process_data(d)

    return {'time': time.strftime('%Y-%m-%d %H:%M:%S'), 'PM2.5': None, 'PM10': None}


def cmd_set_sleep(sleep=1):
    if sleep:
        mode = 0
    else:
        mode = 1

    serial_interface.write(construct_command(CMD_SLEEP, [0x1, mode]))
    read_response()


def cmd_set_working_period(period):
    serial_interface.write(construct_command(CMD_WORKING_PERIOD, [0x1, period]))
    read_response()


def cmd_firmware_ver():
    serial_interface.write(construct_command(CMD_FIRMWARE))
    d = read_response()
    process_version(d)


def cmd_set_id(id):
    id_h = (id >> 8) % 256
    id_l = id % 256
    serial_interface.write(construct_command(CMD_DEVICE_ID, [0] * 10 + [id_l, id_h]))
    read_response()


class AirQualitySensor:

    def __init__(self, output_file_path = None, maximum_file_length = 100):
        self.output_file_path = output_file_path
        self.maximum_file_length = maximum_file_length

    def monitor_air_quality(self, batch_size = 5, reading_period = 2):

        while True:
            cmd_set_sleep(0)
            cmd_set_mode(1)

            batch = []

            for _ in range(batch_size):
                reading = cmd_query_data()
                print(reading)
                batch.append(reading)
                time.sleep(reading_period)

            self.save_batch(batch)
            self.sleep()

    def save_batch(self, batch):

        with open(self.output_file_path, 'a+') as f:
            try:
                data = json.load(f)
            except ValueError:
                data = []

            if self.maximum_file_length:
                if len(data) + len(batch) > self.maximum_file_length:
                    data[0:len(batch)] = batch
                else:
                    data.extend(batch)
            else:
                data.extend(batch)

            json.dump(data, f)

    def sleep(self, sleep_duration = 10):
        print('Going to sleep for {} seconds...'.format(sleep_duration))

        cmd_set_mode(0)
        cmd_set_sleep()
        time.sleep(sleep_duration)


if __name__ == '__main__':
    sensor = AirQualitySensor()
    sensor.monitor_air_quality()
