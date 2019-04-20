from bisect import bisect


class AQICalculator:
    """ A calculator for UK AQI values and bands. These are defined by their lower boundaries (keys) for
    concentrations of PM10 and PM2.5 in micrograms per metre cubed (values) below.
    """
    # https://uk-air.defra.gov.uk/air-pollution/daqi?view=more-info&pollutant=pm25#pollutant
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

    # https://uk-air.defra.gov.uk/air-pollution/daqi?view=more-info&pollutant=pm10#pollutant
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

    aqi_bands_boundaries = {
        1: 'low',
        4: 'moderate',
        7: 'high',
        10: 'very high'
    }

    def calculate_aqis_and_bands(self, reading):
        return reading.extend({
            'PM10 AQI': self._calculate_aqi(reading['PM10'], self.pm10_aqi_lower_boundaries),
            'PM2.5 AQI': self._calculate_aqi(reading['PM2.5'], self.pm25_aqi_lower_boundaries),
            'Overall AQI': max(reading['PM10 AQI'], reading['PM2.5 AQI']),
            'Overall AQI band': self._calculate_aqi_band(reading['Overall AQI'], self.aqi_bands_boundaries)
        })

    @staticmethod
    def _calculate_aqi(concentration, aqi_boundaries):
        aqi_index = bisect(aqi_boundaries.values(), concentration)
        return list(aqi_boundaries.keys())[aqi_index]

    @staticmethod
    def _calculate_aqi_band(aqi, aqi_bands_boundaries):
        aqi_band_index = bisect(aqi_bands_boundaries.values(), aqi)
        return list(aqi_bands_boundaries.keys())[aqi_band_index]
