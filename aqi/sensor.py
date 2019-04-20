#!/usr/bin/python
# coding=utf-8
from __future__ import print_function
import datetime
import time

from aqi.calculator import AQICalculator
from aqi.instruction_set import SensorInstructionSet


class AirQualitySensor:

    modes = {
        'continuous': {
            'measurement_period': 1,
            'monitoring_duration': 10,
            'sleep_time': 0
        },
        'hourly': {
            'measurement_period': 1,
            'monitoring_duration': 600,
            'sleep_time': 3300
        }
    }

    def __init__(self, mode='hourly'):
        self.mode = self.modes[mode]
        self.instruction_set = SensorInstructionSet()
        self.calculator = AQICalculator()

    def __enter__(self):
        self.wake()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sleep()

    def monitor(self):
        """ Monitor the air quality for a given duration, repeating this in an indefinite cycle with a given sleep
        time in between cycles

        :return None:
        """
        start_time = datetime.datetime.now()
        monitoring_duration = datetime.timedelta(seconds=self.mode['monitoring_duration'])

        with self:
            if self.mode['sleep_time'] == 0:
                while True:
                    reading = self.calculator.calculate_aqis_and_bands(self.instruction_set.cmd_query_data())
                    print(reading)
                    time.sleep(self.mode['measurement_period'])

            else:
                while True:
                    time_spent_monitoring = datetime.datetime.now() - start_time

                    if time_spent_monitoring < monitoring_duration:
                        reading = self.calculator.calculate_aqis_and_bands(self.instruction_set.cmd_query_data())
                        print(reading)
                        time.sleep(self.mode['measurement_period'])

                    else:
                        self.sleep()
                        time.sleep(self.mode['sleep_time'])
                        self.wake()

    def wake(self):
        self.instruction_set.cmd_set_sleep(0)
        self.instruction_set.cmd_set_mode(1)

    def sleep(self):
        self.instruction_set.cmd_set_mode(0)
        self.instruction_set.cmd_set_sleep()


if __name__ == '__main__':
    AirQualitySensor().monitor()
