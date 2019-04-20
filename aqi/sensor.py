#!/usr/bin/python
# coding=utf-8
from __future__ import print_function
import datetime
import time

from aqi.calculator import AQICalculator
from aqi.instruction_set import SensorInstructionSet


class AirQualitySensor:

    def __init__(self):
        self.instruction_set = SensorInstructionSet()
        self.calculator = AQICalculator()

    def __enter__(self):
        self.wake()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sleep()

    def monitor(self, measurement_period=1, monitoring_duration=600, sleep_time=3300):
        """ Monitor the air quality for a given duration, repeating this indefinitely after a given sleep time.

        :param int measurement_period: measurement period in seconds
        :param int monitoring_duration: duration in seconds
        :param int sleep_time: sleep time in seconds
        :return None:
        """
        start_time = datetime.datetime.now()
        monitoring_duration = datetime.timedelta(seconds=monitoring_duration)

        while True:
            time_spent_monitoring = datetime.datetime.now() - start_time

            if time_spent_monitoring < monitoring_duration:
                reading = self.calculator.calculate_aqis_and_bands(self.instruction_set.cmd_query_data())
                print(reading)
                time.sleep(measurement_period)

            else:
                time.sleep(sleep_time)

    def wake(self):
        self.instruction_set.cmd_set_sleep(0)
        self.instruction_set.cmd_set_mode(1)

    def sleep(self):
        self.instruction_set.cmd_set_mode(0)
        self.instruction_set.cmd_set_sleep()


if __name__ == '__main__':
    with AirQualitySensor() as sensor:
        sensor.monitor()
