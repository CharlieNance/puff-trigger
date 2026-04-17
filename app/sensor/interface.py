from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SensorReading:
    pm1: float
    pm2_5: float
    pm10: float


class SensorInterface(ABC):
    @abstractmethod
    def read(self) -> SensorReading:
        # Return the latest particulate matter readings from the sensor.
        ...

    @abstractmethod
    def start(self) -> None:
        # Begin continuous sensor polling.
        ...

    @abstractmethod
    def stop(self) -> None:
        # Stop sensor polling and release resources.
        ...
