import json
import os

from aqi import __package_root__
from aqi.sensor import AirQualitySensor


class TestAirQualitySensor:

    test_filename = os.path.join(__package_root__, 'tests', 'test_file.json')

    def test_data_is_saved_when_file_does_not_already_exist(self):
        """ Test data is saved when the file does not already exist.

        :raise AssertionError:
        :return None:
        """
        sensor = AirQualitySensor(mock=True)
        sensor.readings = [{'readings': 'here'}, {'another_one': 'there'}]
        sensor.save_to_file(self.test_filename)

        with open(self.test_filename, 'r') as f:
            data = json.load(f)

        assert data == sensor.readings

        os.remove(self.test_filename)

    def test_data_is_appended_to_existing_data_in_file(self):
        """ Test data is appended to existing data in file.

        :raise AssertionError:
        :return None:
        """
        existing_readings = [{'hello': 'world'}, {'this is': 'a reading'}]

        with open(self.test_filename, 'w') as f:
            json.dump(existing_readings, f)

        sensor = AirQualitySensor(mock = True)
        sensor.readings = [{'more_readings': 'here'}, {'another_one': 'there'}]
        sensor.save_to_file(self.test_filename)
        
        with open(self.test_filename, 'r') as f:
            data = json.load(f)

        assert data == existing_readings + sensor.readings

        os.remove(self.test_filename)
