# Pre-Flight: Questions, Ideas, and Concerns

Things to think through before writing a line of code.

---

## Hardware Questions

**1. How does the PMS5003 communicate with the Pi?**
The PMS5003 uses UART (serial). On the Zero W specifically, the serial port is `/dev/ttyS0` (not `/dev/ttyAMA0`). The `enviroplus` library handles the low-level protocol but the port must be configured correctly when initializing the sensor. Make the serial device path a config value, not a hardcoded string.

**2. What does "detecting a bong hit" actually mean in sensor terms?**
The PMS5003 measures PM1.0, PM2.5, and PM10 particulate matter in µg/m³. Smoke causes a sharp, fast spike. The exact threshold will need real-world tuning — so the trigger parameters (threshold delta, rate-of-change window, cooldown period) must all be runtime-configurable via `.env` or the UI. Start simple (absolute PM2.5 spike), tune from there.

Cooldown is important — smoke dissipates quickly but not instantly, so without a cooldown you'll get repeated triggers on a single event.

**3. Does the Enviro+ HAT physically fit in the setup?**
HAT is seated on GPIO pins and working. M2.5 standoffs still needed for proper mechanical securing — source these before the enclosure phase.

**4. USB speaker setup — RESOLVED**
Speaker is ALSA card 1 on Zero W (was card 2 on the Pi 5 — card numbers are not portable). Volume set to 75%, persisted via `sudo alsactl store`. `~/.asoundrc` configured with card 1 as default. `aplay ~/sounds/smoke_test_output.wav` confirmed working.

**5. Power supply — RESOLVED**
Vilros kit includes an adequate supply. The bigger Zero W power gotcha: the OTG port cannot power the USB speaker alone — a powered USB hub (Huasheng 3-port) is required and in use.

---

## Software / Architecture Questions

**6. What Python version are you targeting?**
Python 3.11 (Raspberry Pi OS Bookworm, 64-bit). Pin this in `.python-version` or `pyproject.toml`.

**7. How will you play audio on Linux? — DECIDED**
`aplay` via subprocess. Dead simple for WAV files, minimal latency, no extra Python dependencies. Wrap it behind an audio interface so the backend can be swapped later without touching call sites.

**8. How do you develop the sensor layer without hardware attached?**
Provide two implementations of the sensor interface: a real one (wraps `enviroplus`/`pms5003`, Pi-only) and a mock one (returns scripted or random readings, works anywhere). The rest of the app only ever imports the interface. This is the most important architectural decision for developer ergonomics.

**9. Event-driven or polling-based sensor reads?**
Start with polling — simpler, easier to test, easier to reason about. The sensor layer can emit events internally when a threshold is crossed, keeping that logic inside the layer and out of the API/audio code.

**10. What gets logged, exactly?**
Proposed schema: `timestamp`, `event_type` (trigger / api / system), `pm1`, `pm2_5`, `pm10`, `audio_file_played`, `notes`

Define this schema before writing the logging layer so you don't refactor it three times.

**11. Should the web UI have any auth?**
Local network only — skip auth for now. Plan a config flag in FastAPI so it can be added later if needed without a structural change.

**12. Split architecture: Svelte on laptop, FastAPI on Pi — DECIDED**
The Zero W (512MB RAM, 1GHz single-core) can't comfortably run a frontend dev server alongside the FastAPI backend and sensor polling. The clean split:

- **Development:** Svelte dev server runs on Windows laptop, makes API calls to `http://chuck-local-pi.local:8000`
- **Production / standalone:** `npm run build` on the laptop, copy the `dist/` output to the Pi, FastAPI serves the static files via `StaticFiles` — no Node.js needed at runtime

This means CORS must be configured in FastAPI from day one.

**13. `pip install enviroplus` vs. git clone**
Use `pip install enviroplus` (Pimoroni now publishes to PyPI). Much cleaner for a FastAPI project. However, some system-level packages still need to be installed manually:

```bash
sudo apt-get install -y python3-smbus i2c-tools libgpiod2
```

Since I2C and UART are already enabled via `raspi-config`, this should be all that's needed beyond the `pip install`.

---

## Ideas for Later Phases

- **Multiple audio clips** — random pick from a pool, or configure playback weights
- **Threshold tuning via UI** — adjust the PM2.5 trigger threshold from the dashboard
- **Air quality history graphs** — chart PM readings over time (already logging it)
- **Cooldown config via UI** — set the post-trigger silence window without touching config files
- **Volume control from UI** — map to `amixer` on the Pi
- **"Now Playing" display** — show what clip just fired in real time via WebSocket (FastAPI → Svelte)
- **Named audio clips with metadata** — friendly names, selectable from the UI
- **Notification mode** — push notification or webhook on trigger
- **UPS HAT / pass-through power bank** — untethered coffee table use
- **Smokey the Bear 3D-printed enclosure** — local library printer

---

## Potential Concerns

**Latency:** The PMS5003 has a ~1 second sample interval. The sound won't fire the instant smoke hits — set expectations accordingly. Still fine for the joke.

**False positives:** Cooking smoke, dust, candles, high humidity can all spike PM readings. The cooldown period helps. Threshold tuning will be important.

**Zero W performance:** 512MB RAM and a single 1GHz core is tight. The FastAPI server + sensor polling + `aplay` subprocess should all be fine, but keep the backend lean. Don't load large audio files into memory — stream/subprocess them.

**ALSA card numbers are not portable:** The speaker is card 1 on the Zero W. If you ever swap hardware, the card number may change. Store it in `.env`.

**`enviroplus` on non-Pi machines:** The package imports will fail on Windows (no GPIO, no I2C). This is why the mock sensor implementation is non-negotiable for the dev workflow.

**Keeping dev and Pi environments in sync:** A `requirements-pi.txt` for Pi-specific packages (`enviroplus`, potentially `RPi.GPIO`) that won't install on Windows. Base `requirements.txt` stays cross-platform.

---

## Suggested Milestones

1. [x] Hardware assembled and confirmed — I2C, UART, audio all working
2. [ ] Install `enviroplus` on Pi, confirm PMS5003 returns readings
3. [ ] Scaffold project structure (folders, module stubs, layer interfaces)
4. [ ] Implement mock sensor — enables all dev work on Windows from this point
5. [ ] Implement audio layer (`aplay` backend) + unit tests
6. [ ] Wire sensor trigger to audio — MVP (smoke in → John Cena out)
7. [ ] FastAPI backend with `/play`, `/sounds`, `/logs`, `/status` endpoints + systemd service
8. [ ] Logging layer (CSV implementation behind interface)
9. [ ] Svelte frontend — dashboard with logs, manual trigger, threshold controls
10. [ ] Integration tests on device
11. [ ] Enclosure design + 3D print
