import subprocess
from app.audio.interface import AudioPlayerInterface
from app.config import config


class AplayPlayer(AudioPlayerInterface):
    # Plays WAV files via aplay subprocess. Linux/Pi only.

    def play(self, filepath: str) -> None:
        # TODO: subprocess.run(["aplay", "-D", f"hw:{config.alsa_card},0", filepath])
        raise NotImplementedError

    def set_volume(self, percent: int) -> None:
        # TODO: subprocess.run(["amixer", "-c", str(config.alsa_card), "sset", "PCM", f"{percent}%"])
        raise NotImplementedError
