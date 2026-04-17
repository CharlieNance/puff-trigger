from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Literal


EventType = Literal["trigger", "api", "system"]


@dataclass
class LogEvent:
    event_type: EventType
    pm1: float | None = None
    pm2_5: float | None = None
    pm10: float | None = None
    audio_file: str | None = None
    notes: str | None = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class LoggerInterface(ABC):
    @abstractmethod
    def log(self, event: LogEvent) -> None:
        # Persist a log event.
        ...

    @abstractmethod
    def get_events(self, limit: int = 100) -> list[LogEvent]:
        # Retrieve the most recent log events.
        ...
