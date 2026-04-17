# Puff Trigger

> Blow a bong hit at a Raspberry Pi and it plays "It's John Cena!" — because why not.

## What Is This

Puff Trigger monitors air quality via the Pimoroni Enviro+ HAT and its PMS5003 particulate matter sensor. When a spike in particulate matter is detected (i.e., smoke blown directly at the sensor), it triggers audio playback through a USB speaker. Phase 1 plays the John Cena entrance audio clip. Future phases will support multiple clips, random selection, and a full web dashboard.

This is a deliberately silly idea built with real software engineering practices — clean architecture, proper test coverage, a REST API, and a Svelte frontend — because dumb projects are more fun when they're done right.

Long-term: a Smokey the Bear-themed 3D-printed enclosure for coffee table display.

## Hardware

| Component | Details |
|---|---|
| Raspberry Pi Zero W | Replaced bricked Pi 5; hostname `chuck-local-pi.local` |
| Enviro+ HAT | Pimoroni PIM458, seated on GPIO pins (M2.5 standoffs needed) |
| Particulate Sensor | PMS5003, communicates over UART (`/dev/ttyS0`) |
| USB Speaker | Jieli UACDemoV1.0, ALSA card 1 |
| USB Hub | Powered 3-port hub required — Zero W OTG can't power the speaker alone |

## Architecture

The Zero W can't comfortably run a frontend dev server, so the system is split:

```
┌────────────────────────────┐        ┌────────────────────────────────────┐
│     Laptop (dev / UI)      │        │     Raspberry Pi Zero W             │
│                            │        │                                     │
│  Svelte Frontend           │◄──────►│  FastAPI Server                     │
│  (dev: Vite dev server)    │  HTTP  │  ├── Sensor Layer (PMS5003)         │
│  (prod: static files       │        │  ├── Audio Layer (aplay)            │
│   served by FastAPI)       │        │  └── Logging Layer (CSV)            │
└────────────────────────────┘        └────────────────────────────────────┘
```

**In production (standalone):** Svelte is built to static files and served by FastAPI directly on the Pi — no Node.js needed at runtime, the Pi just serves HTML/JS.

**Layers:**
- **Sensor Layer** — wraps the `enviroplus` PyPI package; exposes clean events, hides library internals; configurable serial port (`/dev/ttyS0` on Zero W)
- **Audio Layer** — manages audio files, supports named or random playback via `aplay`
- **Logging Layer** — CSV-backed, interface-driven so the transport can be replaced later
- **FastAPI Backend** — REST API connecting all layers; runs as a `systemd` service on the Pi
- **Svelte Frontend** — view logs, run tests, adjust settings, trigger playback manually

## Tech Stack

- Python 3.11 / FastAPI / Uvicorn
- Svelte + Vite
- pytest
- pydub (audio manipulation)
- `enviroplus` (PyPI) + `pms5003`
- python-dotenv

## Repo Structure

```
puff-trigger/
├── app/            ← FastAPI backend (runs on the Pi)
├── frontend/       ← Svelte app (built locally, served by FastAPI in prod)
├── audio/          ← WAV files
├── tests/          ← pytest unit + integration tests
└── pyproject.toml
```

## Setup

### Dev machine (Windows)

```bash
pip install ".[dev]"
```

### Raspberry Pi

Enable required interfaces first (one-time):
```bash
sudo raspi-config nonint do_i2c 0     # enable I2C
sudo raspi-config nonint do_serial 0  # enable UART
# confirm enable_uart=1 is in /boot/config.txt
```

Install system-level dependencies (one-time):
```bash
sudo apt-get install -y python3-smbus i2c-tools libgpiod-dev
```

Clone the repo and install:
```bash
git clone <repo-url>
cd puff-trigger
pip install ".[pi]"
```

Test the sensor import:
```bash
python3 -c "from pms5003 import PMS5003; print('PMS5003 import OK')"
```

### Running (Pi)

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend (dev machine)

```bash
cd frontend
npm install
npm run dev  # Vite dev server, pointed at http://chuck-local-pi.local:8000
```

## Project Status

### Hardware & OS
- [x] Raspberry Pi Zero W set up with SSH key auth
- [x] I2C and UART enabled; Enviro+ HAT detected on I2C bus
- [x] PMS5003 serial port confirmed (`/dev/ttyS0`)
- [x] USB speaker working via powered hub (ALSA card 1, 75% volume persisted)
- [x] Audio playback confirmed with `aplay`
- [ ] M2.5 standoffs sourced to properly secure Enviro+ HAT

### Software
- [ ] Enviro+ library installed and PMS5003 returning readings
- [ ] Project structure scaffolded (sensor / audio / logging / api layers)
- [ ] Sensor layer implementation (real + mock)
- [ ] Audio layer implementation
- [ ] FastAPI backend + systemd service
- [ ] Logging layer
- [ ] Svelte frontend
- [ ] Integration testing on device

### Future
- [ ] Smokey the Bear 3D-printed enclosure
- [ ] UPS HAT or pass-through power bank for untethered use

## Audio Files

Audio clips are `.wav` files stored in the `audio/` directory. New clips can be added using the separate YouTube-to-WAV utility.

## Key Gotchas

- Zero W serial port is `/dev/ttyS0`, **not** `/dev/ttyAMA0`
- Zero W cannot power a USB speaker from OTG alone — powered USB hub required
- `raspi-config nonint` uses `0` = enable, `1` = disable (counterintuitive)
- VS Code Remote SSH is too heavy for the Zero W — use Git Bash SSH directly
- Always seat/remove HATs with Pi fully powered off and unplugged

## License

Personal project. Do whatever you want with it.
