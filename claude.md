# Puff Trigger — Claude Context

## Project Overview

Puff Trigger is a Raspberry Pi Zero W project that detects air quality changes (specifically particulate matter spikes from blowing smoke at the sensor) and triggers audio playback through a connected USB speaker. Phase 1 plays the "It's John Cena!" audio clip. Long-term goal: a Smokey the Bear-themed 3D-printed enclosure.

## Hardware

| Component | Details |
|---|---|
| Raspberry Pi Zero W | hostname `chuck-local-pi.local`, SSH via ED25519 key |
| Pimoroni PIM458 Enviro+ HAT | seated on GPIO; I2C verified (BH1750, ADS1015, BME280 detected) |
| PMS5003 Particulate Sensor | connected to Enviro+ HAT; UART via `/dev/ttyS0` |
| USB Speaker | Jieli UACDemoV1.0; ALSA card 1; volume 75%, persisted via `alsactl store` |
| Powered USB Hub | Huasheng 3-port; required since Zero W OTG can't power the speaker alone |

The `enviroplus` library is installed from PyPI (not git clone). System deps (`python3-smbus`, `i2c-tools`, `libgpiod-dev`) must be installed separately on the Pi.

## Architecture

The Pi Zero W (512MB RAM, 1GHz single-core) cannot run a frontend dev server alongside the backend. The system is split:

- **Pi Zero W:** FastAPI server + sensor layer + audio layer + logging. Runs as a `systemd` service.
- **Dev machine (Windows):** Svelte dev server, calls the Pi's API over the local network.
- **Production/standalone mode:** Svelte is built to static files and served by FastAPI from the Pi directly — no Node.js at runtime.

### Layers

1. **Sensor Layer** — wraps `enviroplus` / `pms5003`; exposes clean events; never leaks library internals. Serial port (`/dev/ttyS0`) must be configurable. Provide a mock implementation so all other layers can be developed and tested on Windows.
2. **Audio Layer** — manages WAV files; supports named or random selection; plays via `aplay` (subprocess). Wrapped behind an interface so the backend can be swapped.
3. **Logging Layer** — interface-first; CSV implementation to start; log sensor triggers, API events, and system events.
4. **FastAPI Backend** — REST API gluing all layers; CORS must be enabled for cross-origin frontend requests; runs on port 8000.
5. **Svelte Frontend** — dashboard: view logs, run/view tests, adjust volume, tune trigger settings, trigger playback manually.

## Repo Structure

```
puff-trigger/
├── app/            ← FastAPI backend (runs on the Pi)
├── frontend/       ← Svelte app (built locally, served by FastAPI in prod)
├── audio/          ← WAV files
├── tests/          ← pytest unit + integration tests
└── pyproject.toml
```

## Dependency Management

Dependencies are declared in `pyproject.toml` with optional groups:

- `pip install ".[dev]"` — dev machine (Windows): base + pytest + httpx + yt-dlp
- `pip install ".[pi]"` — Raspberry Pi: base + enviroplus
- Base deps (cross-platform): fastapi, uvicorn[standard], pydub, python-dotenv, python-multipart

`requirements.txt` is kept as a pinned lock file (`pip freeze` output) — do not manually edit it.

## Tech Stack

- **Language:** Python 3.11 (Raspberry Pi OS Bookworm)
- **Backend:** FastAPI + Uvicorn
- **Frontend:** Svelte + Vite (in `frontend/` subdirectory)
- **Testing:** pytest (unit + integration)
- **Audio:** `aplay` via subprocess, wrapped behind an interface; `pydub` for any manipulation
- **Sensor:** `enviroplus` (PyPI) + `pms5003`
- **Config:** python-dotenv

## Coding Standards

- Well-structured, scalable, testable Python — no single-file hacks
- Interface/wrapper pattern for all third-party integrations (sensor, audio, logging)
- The sensor layer must have a real implementation (Pi hardware) and a mock implementation (dev/test); the rest of the app only ever talks to the interface
- Every layer has unit tests; integration tests cover the sensor-to-audio path
- Keep it clear and easy to follow — irreverence is fine, the code should still be professional
- Do not over-engineer. Start small, expand deliberately.
- CORS must be configured in FastAPI from the start (Svelte frontend origin will differ)
- Configuration (ports, thresholds, serial device, audio path, cooldown) must be in `.env` / dotenv — no hardcoding

## Development Notes

- Developing on Windows, deploying to Pi Zero W; the mock sensor layer bridges this gap
- The Pi Zero W serial port is `/dev/ttyS0`, not `/dev/ttyAMA0` — make this configurable
- VS Code Remote SSH is too heavy for the Zero W; use Git Bash SSH for Pi work
- A `requirements-pi.txt` (or similar split) is needed for Pi-only packages like `enviroplus`
- Audio trigger threshold (PM2.5 delta) and cooldown period should be runtime-configurable, not hardcoded — this will need tuning
- Audio files are WAV format, sourced via a separate YouTube-to-WAV utility
