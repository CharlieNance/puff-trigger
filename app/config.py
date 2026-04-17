import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    serial_port: str = os.getenv("SERIAL_PORT", "/dev/ttyS0")
    alsa_card: int = int(os.getenv("ALSA_CARD", "1"))
    pm25_trigger_threshold: float = float(os.getenv("PM25_TRIGGER_THRESHOLD", "50"))
    trigger_cooldown_seconds: int = int(os.getenv("TRIGGER_COOLDOWN_SECONDS", "10"))
    audio_dir: str = os.getenv("AUDIO_DIR", "audio")
    port: int = int(os.getenv("PORT", "8000"))
    cors_origins: list[str] = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")


config = Config()
