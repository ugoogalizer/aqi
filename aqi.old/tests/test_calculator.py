import pytest

from aqi.calculator import AQICalculator


class TestCalculator:


    @pytest.mark.parametrize('concentration, expected_aqi', [
        (0, 1),
        (1, 1),
        (16.9, 1),
        (17, 2),
        (33, 2),
        (100, 9),
        (101, 10)
    ])
    def test_calculate_pm10_aqi(self, concentration, expected_aqi):
        calculator = AQICalculator()
        aqi = calculator._calculate_aqi(concentration, calculator.pm10_aqi_lower_boundaries)
        assert aqi == expected_aqi

    @pytest.mark.parametrize('concentration, expected_aqi', [
        (0, 1),
        (1, 1),
        (11.9, 1),
        (17, 2),
        (33, 3),
        (70, 9),
        (100, 10)
    ])
    def test_calculate_pm25_aqi(self, concentration, expected_aqi):
        calculator = AQICalculator()
        aqi = calculator._calculate_aqi(concentration, calculator.pm25_aqi_lower_boundaries)
        assert aqi == expected_aqi

    @pytest.mark.parametrize('band, expected_band', [
        (1, 'low'),
        (3, 'low'),
        (4, 'moderate'),
        (7, 'high'),
        (10, 'very high')
    ])
    def test_calculate_aqi_band(self, band, expected_band):
        calculator = AQICalculator()
        band = calculator._calculate_aqi_band(band, calculator.aqi_bands_boundaries)
        assert band == expected_band
