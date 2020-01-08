class Reading:

    def __init__(self, time, pm25, pm25_aqi, pm10, pm10_aqi, overall_aqi, overall_aqi_band):

        self.time = time
        self.pm25 = pm25
        self.pm25_aqi = pm25_aqi
        self.pm10 = pm10
        self.pm10_aqi = pm10_aqi
        self.overall_aqi = overall_aqi
        self.overall_aqi_band = overall_aqi_band

    def to_dict(self):
        return {
            'Time': self.time,
            'PM2.5': self.pm25,
            'PM2.5 AQI': self.pm25_aqi,
            'PM10': self.pm10,
            'PM10 AQI': self.pm10_aqi,
            'Overall AQI': self.overall_aqi,
            'Overall AQI Band': self.overall_aqi_band
        }

    @classmethod
    def from_dict(cls, dictionary):
        return cls(
            time=dictionary['Time'],
            pm25=dictionary['PM2.5'],
            pm25_aqi=dictionary['PM2.5 AQI'],
            pm10=dictionary['PM10'],
            pm10_aqi=dictionary['PM10 AQI'],
            overall_aqi=dictionary['Overall AQI'],
            overall_aqi_band=['Overall AQI Band']
        )
