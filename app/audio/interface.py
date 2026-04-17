from abc import ABC, abstractmethod


class AudioPlayerInterface(ABC):
    @abstractmethod
    def play(self, filepath: str) -> None:
        # Play a WAV file by absolute or relative path.
        ...

    @abstractmethod
    def set_volume(self, percent: int) -> None:
        # Set playback volume 0–100.
        ...
