# coding=utf-8
import logging
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

    logger = logging.getLogger(__name__)

    def __init__(self, mock=False):

        if not mock:
            self.serial_interface = serial.Serial()
            self.serial_interface.port = '/dev/ttyUSB0'
            self.serial_interface.baudrate = 9600
            self.serial_interface.open()
            self.serial_interface.flushInput()

    @staticmethod
    def dump(data, prefix=''):
        print((prefix + ' '.join(x.encode('hex') for x in data)))

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

    @staticmethod
    def process_data(data):
        r = struct.unpack('<HHxxBB', data[2:])

        reading = {
            'Time': time.strftime('%d.%m.%Y %H:%M:%S'),
            'PM2.5': r[0] / 10.0,
            'PM10': r[1] / 10.0
        }

        return reading
        # checksum = sum(ord(v) for v in data[2:8]) % 256
        # print('PM 2.5: {} μg/m^3  PM 10: {} μg/m^3 CRC={}'.format(pm25, pm10, 'OK' if (checksum==r[2] and r[ 3]==0xab) else 'NOK'))

    @staticmethod
    def process_version(data):
        r = struct.unpack('<BBBHBB', data[3:])
        checksum = sum(ord(v) for v in data[2:8]) % 256
        print((
            'Y: {}, M: {}, D: {}, ID: {}, CRC={}'
            .format(r[0], r[1], r[2], hex(r[3]), 'OK' if (checksum == r[4] and r[5] == 0xab) else 'NOK')
        ))

    def read_response(self):
        byte = 0

        while byte != '\xaa':
            byte = self.serial_interface.read(size=1)

        data = self.serial_interface.read(size=9)

        if self.DEBUG:
            self.dump(data, '< ')

        return byte + data

    def set_mode(self, mode=MODE_QUERY):
        self.serial_interface.write(self.construct_command(self.CMD_MODE, [0x1, mode]))
        self.read_response()

    def query_data(self):
        self.serial_interface.write(self.construct_command(self.CMD_QUERY_DATA))
        response = self.read_response()

        if response[1] == '\xc0':
            return self.process_data(response)

        return {'Time': time.strftime('%Y-%m-%d %H:%M:%S'), 'PM2.5': None, 'PM10': None}

    def sleep(self):
        """ Send the sensor to sleep.

        :return None:
        """
        self.logger.debug('Sending sensor to sleep.')
        mode = 0
        self.set_mode(mode)
        self.serial_interface.write(self.construct_command(self.CMD_SLEEP, [0x1, mode]))
        self.read_response()

    def wake(self):
        """ Wake the sensor.

        :return None:
        """
        self.logger.debug('Waking sensor up.')
        mode = 1
        self.serial_interface.write(self.construct_command(self.CMD_SLEEP, [0x1, mode]))
        self.read_response()
        self.set_mode(mode)

    def set_working_period(self, period):
        self.serial_interface.write(self.construct_command(self.CMD_WORKING_PERIOD, [0x1, period]))
        self.read_response()

    def get_firmware_version(self):
        """ Get the firmware version and print it.

        :return None:
        """
        self.serial_interface.write(self.construct_command(self.CMD_FIRMWARE))
        response = self.read_response()
        self.process_version(response)

    def set_id(self, id_):
        id_h = (id_ >> 8) % 256
        id_l = id_ % 256
        self.serial_interface.write(self.construct_command(self.CMD_DEVICE_ID, [0] * 10 + [id_l, id_h]))
        self.read_response()
