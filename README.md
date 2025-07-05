# FlexGrid Firmware (V1.0)

MicroPython firmware for the ESP32-S3 “FlexGrid V1.0” pressure-sensor matrix controller, part of the OpenMuscle project.

---

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Hardware Requirements](#hardware-requirements)  
- [Software Requirements](#software-requirements)  
- [Getting Started](#getting-started)  
  - [Repository Structure](#repository-structure)  
  - [Flashing the Device](#flashing-the-device)  
- [Configuration](#configuration)  
- [Usage](#usage)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Overview

This repository contains the MicroPython firmware for the FlexGrid V1.0:  
a 16×4 Velostat pressure-sensor matrix driven by an ESP32-S3. It samples the matrix asynchronously, broadcasts the data via UDP over Wi-Fi, and provides a simple two-button menu interface (with on-screen or REPL-based configuration).

---

## Features

- **Async sensor scanning** of a 16 (columns) × 4 (rows) matrix via a 4-bit MUX and ADC1 channels  
- **Wi-Fi + UDP** networking for real-time data streaming  
- **SSD1306** OLED menu/UI (fallback to REPL logging if display is absent)  
- **Two-button** navigation and on-device configuration (Wi-Fi & UDP target)  
- **Centralized logger** with `[DBG]`, `[INF]`, `[WRN]`, `[ERR]` levels  
- **Modular** code organization: `sensor_matrix`, `network_manager`, `display_manager`, `menu_manager`, `settings_manager`, `logger`

---

## Hardware Requirements

- ESP32-S3 WROOM-1 (N16-R8) module  
- 16-channel analog MUX (e.g. CD74HC4067)  
- Velostat pressure-sensor matrix (16×4)  
- Two momentary push-buttons  
- SSD1306 I²C OLED display (optional)

---

## Software Requirements

- [MicroPython for ESP32-S3](https://micropython.org/download/esp32-s3/)  
- [`mpremote`](https://pypi.org/project/mpremote/) or [Thonny IDE](https://thonny.org/)  
- (Optional) `ssd1306.py` driver in `/lib`

---

## Getting Started

### Repository Structure

```
/
├── boot.py
├── flexgrid.py
├── config/
│   └── settings.json
└── lib/
    ├── display_manager.py
    ├── logger.py
    ├── menu_manager.py
    ├── network_manager.py
    ├── sensor_matrix.py
    ├── settings_manager.py
    └── ssd1306.py        ← copy from your driver source
```

### Flashing the Device

1. Install MicroPython onto your ESP32-S3 using esptool and [these instructions](https://micropython.org/download/ESP32_GENERIC_S3/).
2. Copy the repository contents to the device flash:
   ```bash
   mpremote connect /dev/ttyUSB0 fs cp -r . :/
   ```
3. Reboot:  
   ```bash
   mpremote connect /dev/ttyUSB0 reset
   ```

---

## Configuration

The first time you boot, a default `config/settings.json` is created:
```json
{
  "wifi_ssid": "",
  "wifi_password": "",
  "udp_target_ip": "192.168.1.100",
  "udp_port": 4210
}
```
Use the on-device menu (or REPL `input()`) to set your Wi-Fi credentials and UDP target.

---

## Usage

- **Boot**: `boot.py` schedules `flexgrid.main()` on the asyncio loop.  
- **Async loops**:
  - `sensor_loop` reads and sends matrix data every 100 ms.  
  - `display_loop` refreshes the UI every 250 ms.  
  - `menu_loop` polls buttons every 50 ms.  
- **Logs** appear on the REPL prefixed by log level.

---

## Contributing

1. Fork the repo.  
2. Create a feature branch (`git checkout -b feature/foo`).  
3. Commit your changes (`git commit -am "Add foo"`).  
4. Push to the branch (`git push origin feature/foo`).  
5. Open a Pull Request.

Please adhere to the existing code style, include meaningful log statements, and update the README as needed.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
