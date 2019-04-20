#!/usr/bin/python
# coding=utf-8
from __future__ import print_function
from bisect import bisect
import time

from aqi.instruction_set import SensorInstructionSet

# UK AQI lower boundaries (keys) for concentrations of PM10 and PM2.5 in micrograms per metre cubed (values)
pm10_aqi_lower_boundaries = {
    1: 0,
    2: 17,
    3: 34,
    4: 51,
    5: 59,
    6: 67,
    7: 76,
    8: 84,
    9: 92,
    10: 101
}

pm25_aqi_lower_boundaries = {
    1: 0,
    2: 12,
    3: 24,
    4: 36,
    5: 42,
    6: 48,
    7: 54,
    8: 59,
    9: 65,
    10: 71
}


class AirQualitySensor:

    def __init__(self, output_file_path = None, maximum_file_length = 100):
        self.output_file_path = output_file_path
        self.maximum_file_length = maximum_file_length

        self.instruction_set = SensorInstructionSet()

    def __enter__(self):
        self.wake()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sleep()

    def monitor(self, reading_spacing = 2):
        while True:
            reading = self.instruction_set.cmd_query_data()
            reading['PM10 AQI'] = self.calculate_aqi(reading['PM10'], pm10_aqi_lower_boundaries)
            reading['PM2.5 AQI'] = self.calculate_aqi(reading['PM2.5'], pm25_aqi_lower_boundaries)
            print(reading)
            time.sleep(reading_spacing)

    @staticmethod
    def calculate_aqi(concentration, boundaries):
        aqi_index = bisect(boundaries.values(), concentration)
        return list(boundaries.keys())[aqi_index]

    def wake(self):
        self.instruction_set.cmd_set_sleep(0)
        self.instruction_set.cmd_set_mode(1)

    def sleep(self):
        self.instruction_set.cmd_set_mode(0)
        self.instruction_set.cmd_set_sleep()


if __name__ == '__main__':
    with AirQualitySensor() as sensor:
        sensor.monitor()
