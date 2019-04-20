#!/usr/bin/python
# coding=utf-8
from __future__ import print_function
import datetime
import time

from aqi.calculator import AQICalculator
from aqi.instruction_set import SensorInstructionSet


class SensorMode:

    def __init__(self, measurement_period, monitoring_duration, sleep_time):
        """ Define a mode for an AirQualitySensor

        :param int measurement_period: inverse of measurement frequency; measured in seconds
        :param int|None monitoring_duration: duration to monitor for in seconds
        :param int sleep_time: duration to sleep for between monitoring sessions; measured in seconds
        """
        self.measurement_period = measurement_period
        self.monitoring_duration = datetime.timedelta(seconds=monitoring_duration)
        self.sleep_time = sleep_time


class AirQualitySensor:

    modes = {
        'continuous': SensorMode(measurement_period=1, monitoring_duration=None, sleep_time=0),
        'hourly_five_minute_measurement': SensorMode(measurement_period=1, monitoring_duration=600, sleep_time=3300),
        'hourly': SensorMode(measurement_period=1, monitoring_duration=1, sleep_time=3599)
    }

    def __init__(self, mode='hourly_five_minute_measurement'):
        self.mode = self.modes[mode]
        self.instruction_set = SensorInstructionSet()
        self.calculator = AQICalculator()

    def __enter__(self):
        self._wake()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._sleep()

    def monitor(self):
        """ Monitor the air quality for a given duration, repeating this in an indefinite cycle with a given sleep
        time in between cycles

        :return None:
        """
        start_time = datetime.datetime.now()

        with self:
            if self.mode['sleep_time'] == 0:
                while True:
                    self._take_measurement()

            else:
                while True:
                    time_spent_monitoring = datetime.datetime.now() - start_time

                    if time_spent_monitoring < self.mode.monitoring_duration:
                        self._take_measurement()

                    else:
                        self._sleep()
                        time.sleep(self.mode.sleep_time)
                        self._wake()

    def _take_measurement(self):
        """ Take a measurement at the period set in the mode.

        :return None:
        """
        reading = self.calculator.calculate_aqis_and_bands(self.instruction_set.cmd_query_data())
        print(reading)
        time.sleep(self.mode.measurement_period)

    def _wake(self):
        """ Wake the sensor.

        :return None:
        """
        self.instruction_set.cmd_set_sleep(0)
        self.instruction_set.cmd_set_mode(1)

    def _sleep(self):
        """ Send the sensor to sleep.

        :return None:
        """
        self.instruction_set.cmd_set_mode(0)
        self.instruction_set.cmd_set_sleep()


if __name__ == '__main__':
    AirQualitySensor(mode='hourly_five_minute_measurement').monitor()
