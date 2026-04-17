# 🚨 Bong Rip Smoke Detector — Project Summary

## What Is This

A Raspberry Pi Zero W-based smoke detector that plays a sound bite when it detects particulate matter (i.e. someone blowing a bong hit at it). Uses a Pimoroni PIM458 Enviro+ Air Quality HAT with a PMS5003 particulate sensor to detect smoke, and a USB speaker to play the audio response.

Long term goal is a "Smokey the Bear"-style 3D-printed enclosure for coffee table display.

---

## Hardware

| Component                         | Notes                                                                    |
| --------------------------------- | ------------------------------------------------------------------------ |
| Raspberry Pi Zero W               | Replaced a Pi 5 that was bricked during setup                            |
| Pimoroni PIM458 Enviro+ HAT       | Seated on GPIO pins, needs M2.5 standoffs for proper mechanical securing |
| PMS5003 Particulate Sensor        | Connected to Enviro+ HAT, communicates over UART                         |
| USB Speaker (Jieli UACDemoV1.0)   | card 1 on this setup                                                     |
| Powered USB Hub (Huasheng 3-port) | Required — Zero W can't power speaker from OTG port alone                |

**Pi connection details:**
- Username: `chuckniddy` | Hostname: `chuck-local-pi.local`
- SSH: ED25519 key-based auth

---

## What's Been Completed

### Hardware & OS
- [x] Flashed fresh OS via Raspberry Pi Imager, SSH key configured
- [x] SSH access confirmed working from Windows Git Bash
- [x] Cleared stale host key from `known_hosts` after reflash (`ssh-keygen -R chuck-local-pi.local`)
- [x] I2C enabled (`sudo raspi-config nonint do_i2c 0`)
- [x] Enviro+ HAT verified on I2C bus — three chips detected:
  - `0x23` — BH1750 light sensor
  - `0x49` — ADS1015 ADC
  - `0x76` — BME280 temp/pressure/humidity
- [x] Serial/UART enabled for PMS5003 (`/dev/serial0` → `/dev/ttyS0`)
- [x] `enable_uart=1` added to `/boot/config.txt`

### Audio
- [x] USB speaker detected via powered USB hub on OTG port
- [x] Speaker is **card 1** (`hw:1,0`) on Zero W — different from Pi 5 setup (was card 2)
- [x] ALSA volume set: `amixer -c 1 sset 'PCM' 75%`
- [x] Settings persisted: `sudo alsactl store`
- [x] `~/.asoundrc` configured with card 1 as default
- [x] Audio playback confirmed: `aplay -D hw:1,0 ~/sounds/smoke_test_output.wav` ✅

---

## Key Gotchas & Lessons Learned

- `raspi-config nonint` uses `0` = enable, `1` = disable — counterintuitive
- Zero W serial port is `/dev/serial0` / `/dev/ttyS0`, **not** `/dev/ttyAMA0`
- Zero W cannot power a USB speaker from the OTG port alone — powered USB hub required
- VS Code Remote SSH terminal is too heavy for the Zero W — use Git Bash SSH instead
- Always seat/remove HATs with Pi fully powered off and unplugged
- M2.5 standoffs needed to properly secure the Enviro+ HAT mechanically

---

## Next Steps

- [ ] Install Pimoroni Enviro+ Python library
- [ ] Verify PMS5003 sensor is returning particulate readings
- [ ] Build Fast API audio server with `/play/<filename>` and `/sounds` endpoints
- [ ] Write smoke detection logic (threshold-based trigger on PM2.5 readings)
- [ ] Wire sensor trigger to audio playback
- [ ] Run Fast API as a systemd service
- [ ] Source M2.5 standoffs to properly secure Enviro+ HAT
- [ ] Design and 3D-print enclosure (Smokey the Bear theme, local library printer)
- [ ] Consider UPS HAT or pass-through power bank for untethered coffee table use
