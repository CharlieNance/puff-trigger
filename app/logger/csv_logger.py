import csv
import os
from app.logger.interface import LoggerInterface, LogEvent

FIELDS = ["timestamp", "event_type", "pm1", "pm2_5", "pm10", "audio_file", "notes"]


class CsvLogger(LoggerInterface):
    # Appends log events to a CSV file. One file per day is a reasonable
    # extension, but start simple: one file total.

    def __init__(self, filepath: str = "logs/events.csv"):
        self._filepath = filepath
        self._ensure_file()

    def log(self, event: LogEvent) -> None:
        # TODO: open in append mode, write a row using FIELDS
        raise NotImplementedError

    def get_events(self, limit: int = 100) -> list[LogEvent]:
        # TODO: read CSV, return the last `limit` rows as LogEvent objects
        raise NotImplementedError

    def _ensure_file(self) -> None:
        # TODO: create the file with headers if it doesn't exist yet
        raise NotImplementedError
