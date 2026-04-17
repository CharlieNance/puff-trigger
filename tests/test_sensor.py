from app.sensor.mock import MockSensor
from app.sensor.interface import SensorReading


def test_mock_sensor_returns_reading():
    sensor = MockSensor()
    reading = sensor.read()
    assert isinstance(reading, SensorReading)
    assert reading.pm2_5 >= 0


def test_mock_sensor_spike():
    sensor = MockSensor(spike_on_read=2)
    sensor.read()
    spike = sensor.read()
    assert spike.pm2_5 > 100
