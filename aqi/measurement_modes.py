import datetime


class MeasurementMode:

    def __init__(self, name, measurement_period, monitoring_duration, sleep_time, aggregation=''):
        """ Define a measurement mode for an AirQualitySensor.

        :param str name:
        :param float measurement_period: inverse of measurement frequency; measured in seconds
        :param float|None monitoring_duration: duration to monitor for in seconds
        :param float sleep_time: duration to sleep for between monitoring sessions; measured in seconds
        :param str aggregation: name of aggregation to carry out at monitoring period end
        """
        self.name = name
        self.measurement_period = measurement_period
        self.monitoring_duration = None if monitoring_duration is None else datetime.timedelta(
            seconds=monitoring_duration
        )
        self.sleep_time = sleep_time
        self.aggregation = aggregation

    def __repr__(self):
        return (
            '<{}(name={!r}, measurement_period={!r}, monitoring_duration={!r}, sleep_time={!r}, '
            'aggregation={!r})>'
            .format(
                self.__class__.__name__,
                self.name,
                self.measurement_period,
                self.monitoring_duration,
                self.sleep_time,
                self.aggregation
            )
        )


modes = {
    'continuous': MeasurementMode(
        name='continuous',
        measurement_period=1,
        monitoring_duration=None,
        sleep_time=0
    ),
    'hourly': MeasurementMode(
        name='hourly',
        measurement_period=1,
        monitoring_duration=1,
        sleep_time=3599
    ),
    'hourly_five_minute_average': MeasurementMode(
        name='hourly_five_minute_average',
        measurement_period=1,
        monitoring_duration=300,
        sleep_time=3300,
        aggregation='mean'
    )
}
