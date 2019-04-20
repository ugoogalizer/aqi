from bisect import bisect
from collections import OrderedDict


class AQICalculator:
    """ A calculator for UK AQI values and bands. These are defined by their lower boundaries (keys) for
    concentrations of PM10 and PM2.5 in micrograms per metre cubed (values) below.
    """

    # https://uk-air.defra.gov.uk/air-pollution/daqi?view=more-info&pollutant=pm10#pollutant
    pm10_aqi_lower_boundaries = OrderedDict({
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
    })

    # https://uk-air.defra.gov.uk/air-pollution/daqi?view=more-info&pollutant=pm25#pollutant
    pm25_aqi_lower_boundaries = OrderedDict({
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
    })

    aqi_bands_boundaries = OrderedDict({
        'low': 1,
        'moderate': 4,
        'high': 7,
        'very high': 10
    })

    def calculate_aqis_and_bands(self, reading):
        return reading.extend({
            'PM10 AQI': self._calculate_aqi(reading['PM10'], self.pm10_aqi_lower_boundaries),
            'PM2.5 AQI': self._calculate_aqi(reading['PM2.5'], self.pm25_aqi_lower_boundaries),
            'Overall AQI': max(reading['PM10 AQI'], reading['PM2.5 AQI']),
            'Overall AQI band': self._calculate_aqi_band(reading['Overall AQI'], self.aqi_bands_boundaries)
        })

    @staticmethod
    def _calculate_aqi(concentration, aqi_boundaries):
        for aqi_value, lower_boundary in reversed(aqi_boundaries.items()):
            if concentration < lower_boundary:
                continue
            return aqi_value
        raise ValueError('Concentration value {} out of possible range'.format(concentration))

    @staticmethod
    def _calculate_aqi_band(aqi, aqi_bands_boundaries):
        for aqi_band, lower_boundary in reversed(aqi_bands_boundaries.items()):
            if aqi < lower_boundary:
                continue
            return aqi_band

        raise ValueError('AQI value {} out of possible range of AQIs'.format(aqi))
