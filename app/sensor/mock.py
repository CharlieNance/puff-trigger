import random
from app.sensor.interface import SensorInterface, SensorReading


class MockSensor(SensorInterface):
    # Returns scripted or randomized readings for dev and testing.
    # Drop-in replacement for EnviroSensor — no hardware required.

    def __init__(self, spike_on_read: int | None = None):
        self._read_count = 0
        self._spike_on_read = spike_on_read  # force a trigger on the Nth read

    def read(self) -> SensorReading:
        self._read_count += 1
        if self._spike_on_read and self._read_count == self._spike_on_read:
            return SensorReading(pm1=180.0, pm2_5=250.0, pm10=300.0)
        return SensorReading(
            pm1=round(random.uniform(1.0, 5.0), 1),
            pm2_5=round(random.uniform(2.0, 8.0), 1),
            pm10=round(random.uniform(3.0, 12.0), 1),
        )

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass
