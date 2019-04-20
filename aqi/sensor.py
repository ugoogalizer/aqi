#!/usr/bin/python
# coding=utf-8
from __future__ import print_function
import time

from aqi.calculator import AQICalculator
from aqi.instruction_set import SensorInstructionSet


class AirQualitySensor:

    def __init__(self, output_file_path = None, maximum_file_length = 100):
        self.output_file_path = output_file_path
        self.maximum_file_length = maximum_file_length
        self.instruction_set = SensorInstructionSet()
        self.calculator = AQICalculator()

    def __enter__(self):
        self.wake()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sleep()

    def monitor(self, reading_spacing = 2):
        while True:
            reading = self.calculator.calculate_aqis_and_bands(self.instruction_set.cmd_query_data())
            print(reading)
            time.sleep(reading_spacing)

    def wake(self):
        self.instruction_set.cmd_set_sleep(0)
        self.instruction_set.cmd_set_mode(1)

    def sleep(self):
        self.instruction_set.cmd_set_mode(0)
        self.instruction_set.cmd_set_sleep()


if __name__ == '__main__':
    with AirQualitySensor() as sensor:
        sensor.monitor()
