# coding=utf-8

import serial
import struct
import time


class SensorInstructionSet:
    """ Instruction set for SDS011 particle sensor."""

    DEBUG = 0
    CMD_MODE = 2
    CMD_QUERY_DATA = 4
    CMD_DEVICE_ID = 5
    CMD_SLEEP = 6
    CMD_FIRMWARE = 7
    CMD_WORKING_PERIOD = 8
    MODE_ACTIVE = 0
    MODE_QUERY = 1

    data = ''

    def __init__(self):

        self.serial_interface = serial.Serial()
        self.serial_interface.port = '/dev/ttyUSB0'
        self.serial_interface.baudrate = 9600

        self.serial_interface.open()
        self.serial_interface.flushInput()

    def dump(self, data, prefix=''):
        print(prefix + ' '.join(x.encode('hex') for x in data))

    def construct_command(self, command, data=None):
        data = data or []
        assert len(data) <= 12
        data += [0] * (12 - len(data))
        checksum = (sum(data) + command - 2) % 256
        ret = '\xaa\xb4' + chr(command)
        ret += ''.join(chr(x) for x in data)
        ret += '\xff\xff' + chr(checksum) + '\xab'

        if self.DEBUG:
            self.dump(ret, '> ')
        return ret

    def process_data(self, data):
        r = struct.unpack('<HHxxBB', data[2:])
        pm25 = r[0] / 10.0
        pm10 = r[1] / 10.0
        checksum = sum(ord(v) for v in data[2:8]) % 256
        return {'time': time.strftime('%d.%m.%Y %H:%M:%S'), 'PM2.5': pm25, 'PM10': pm10}
        #print('PM 2.5: {} μg/m^3  PM 10: {} μg/m^3 CRC={}'.format(pm25, pm10, 'OK' if (checksum==r[2] and r[3]==0xab) else 'NOK'))

    def process_version(self, d):
        r = struct.unpack('<BBBHBB', d[3:])
        checksum = sum(ord(v) for v in d[2:8]) % 256
        print(
            'Y: {}, M: {}, D: {}, ID: {}, CRC={}'
            .format(r[0], r[1], r[2], hex(r[3]), 'OK' if (checksum == r[4] and r[5] == 0xab) else 'NOK')
        )

    def read_response(self):
        byte = 0

        while byte != '\xaa':
            byte = self.serial_interface.read(size=1)

        data = self.serial_interface.read(size=9)

        if self.DEBUG:
            self.dump(data, '< ')

        return byte + data

    def cmd_set_mode(self, mode=MODE_QUERY):
        self.serial_interface.write(self.construct_command(self.CMD_MODE, [0x1, mode]))
        self.read_response()

    def cmd_query_data(self):
        self.serial_interface.write(self.construct_command(self.CMD_QUERY_DATA))
        d = self.read_response()

        if d[1] == '\xc0':
            return self.process_data(d)

        return {'time': time.strftime('%Y-%m-%d %H:%M:%S'), 'PM2.5': None, 'PM10': None}

    def cmd_set_sleep(self, sleep=1):
        if sleep:
            mode = 0
        else:
            mode = 1

        self.serial_interface.write(self.construct_command(self.CMD_SLEEP, [0x1, mode]))
        self.read_response()

    def cmd_set_working_period(self, period):
        self.serial_interface.write(self.construct_command(self.CMD_WORKING_PERIOD, [0x1, period]))
        self.read_response()

    def cmd_firmware_ver(self):
        self.serial_interface.write(self.construct_command(self.CMD_FIRMWARE))
        d = self.read_response()
        self.process_version(d)

    def cmd_set_id(self, id_):
        id_h = (id_ >> 8) % 256
        id_l = id_ % 256
        self.serial_interface.write(self.construct_command(self.CMD_DEVICE_ID, [0] * 10 + [id_l, id_h]))
        self.read_response()
