# Pi-only: requires the enviroplus package (pip install ".[pi]")
from app.sensor.interface import SensorInterface, SensorReading


class EnviroSensor(SensorInterface):
    # Wraps the pms5003 library to read particulate matter from the
    # Pimoroni Enviro+ HAT. Serial port is configurable via config.serial_port.

    def read(self) -> SensorReading:
        # TODO: initialize PMS5003, return SensorReading
        raise NotImplementedError

    def start(self) -> None:
        # TODO: start PMS5003 polling loop
        raise NotImplementedError

    def stop(self) -> None:
        # TODO: stop PMS5003 and close serial connection
        raise NotImplementedError
