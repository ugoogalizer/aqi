import json
import os

from aqi import __package_root__
from aqi.sensor import AirQualitySensor


class TestAirQualitySensor:

    def test_data_is_appended_to_existing_data_in_file(self):
        """ Test data is appended to existing data in file.

        :raise AssertionError:
        :return None:
        """
        existing_readings = [{'hello': 'world'}, {'this is': 'a reading'}]

        test_filename = os.path.join(__package_root__, 'tests', 'test_file.json')

        with open(test_filename, 'w') as f:
            json.dump(existing_readings, f)

        sensor = AirQualitySensor(mock = True)
        sensor.readings = [{'more_readings': 'here'}, {'another_one': 'there'}]
        sensor.save_to_file(test_filename)
        
        with open(test_filename, 'r') as f:
            data = json.load(f)

        assert data == existing_readings + sensor.readings

        os.remove(test_filename)
