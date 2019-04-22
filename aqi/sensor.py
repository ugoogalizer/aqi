from __future__ import print_function
import datetime
import json
import os
import time

from aqi.calculator import AQICalculator
from aqi.instruction_set import SensorInstructionSet


READINGS_FILE = 'readings.json'


class SensorMode:

    def __init__(self, name, measurement_period, monitoring_duration, sleep_time):
        """ Define a mode for an AirQualitySensor

        :param str name:
        :param float measurement_period: inverse of measurement frequency; measured in seconds
        :param float|None monitoring_duration: duration to monitor for in seconds
        :param float sleep_time: duration to sleep for between monitoring sessions; measured in seconds
        """
        self.name = name
        self.measurement_period = measurement_period
        self.monitoring_duration = None if monitoring_duration is None else datetime.timedelta(seconds=monitoring_duration)
        self.sleep_time = sleep_time

    def __repr__(self):
        return '<{}(name={!r}, measurement_period={!r}, monitoring_duration={!r}, sleep_time={!r})>'.format(
            self.__class__.__name__,
            self.name,
            self.measurement_period,
            self.monitoring_duration,
            self.sleep_time
        )


class AirQualitySensor:

    modes = {
        'continuous': SensorMode(
            name='continuous',
            measurement_period=1,
            monitoring_duration=None,
            sleep_time=0
        ),
        'hourly': SensorMode(
            name='hourly',
            measurement_period=1,
            monitoring_duration=1,
            sleep_time=3599
        ),
        'hourly_five_minute_measurement': SensorMode(
            name='hourly_five_minute_measurement',
            measurement_period=1,
            monitoring_duration=300,
            sleep_time=3300
        )
    }

    def __init__(self, mode='hourly_five_minute_measurement', mock=False):
        self.mode = self.modes[mode]
        self.instruction_set = SensorInstructionSet(mock=mock)
        self.calculator = AQICalculator()
        self.readings = []

    def __enter__(self):
        self._wake()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._sleep()
        self.save_readings_to_file(READINGS_FILE)

    def monitor(self):
        """ Monitor the air quality according to the mode selected.

        :return None:
        """
        print(self.mode)

        start_time = datetime.datetime.now()

        with self:
            if self.mode.sleep_time == 0:
                while True:
                    self.take_reading()

            else:
                while True:
                    time_spent_monitoring = datetime.datetime.now() - start_time

                    # if time_spent_monitoring % datetime.timedelta(seconds = 300) == 0:
                    self.save_readings_to_file(READINGS_FILE)

                    if self.mode.monitoring_duration:
                        if time_spent_monitoring < self.mode.monitoring_duration:
                            self.take_reading()

                        else:
                            self._sleep()
                            time.sleep(self.mode.sleep_time)
                            self._wake()

                    else:
                        self.take_reading()

    def take_reading(self):
        """ Take a reading of the air quality.

        :return None:
        """
        reading = self.calculator.calculate_aqis_and_bands(self.instruction_set.cmd_query_data())
        self.readings.append(reading)
        print(reading)
        time.sleep(self.mode.measurement_period)

    def save_readings_to_file(self, path):
        """ Save readings to a file, appending to any readings already in the file.

        :param str path:
        :return None:
        """
        if not os.path.exists(path):
            open(path, 'w+').close()

        with open(path, 'r') as f:
            try:
                existing_data = json.load(f)
            except:
                existing_data = []

        all_data = existing_data + self.readings

        with open(path, 'w') as f:
            json.dump(all_data, f)

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
