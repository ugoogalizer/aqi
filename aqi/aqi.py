#!/usr/bin/python
# coding=utf-8
from __future__ import print_function
import json
import time

from aqi.instruction_set import SensorInstructionSet


class AirQualitySensor:

    def __init__(self, output_file_path = None, maximum_file_length = 100):
        self.output_file_path = output_file_path
        self.maximum_file_length = maximum_file_length

        self.instruction_set = SensorInstructionSet()

    def monitor(self, batch_size = 5, reading_period = 2):

        while True:
            self.wake()

            batch = []

            for _ in range(batch_size):
                reading = self.instruction_set.cmd_query_data()
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

            data.extend(batch)
            json.dump(data, f)

    def wake(self):
        self.instruction_set.cmd_set_sleep(0)
        self.instruction_set.cmd_set_mode(1)

    def sleep(self):
        self.instruction_set.cmd_set_mode(0)
        self.instruction_set.cmd_set_sleep()


if __name__ == '__main__':
    sensor = AirQualitySensor()
    sensor.monitor()
