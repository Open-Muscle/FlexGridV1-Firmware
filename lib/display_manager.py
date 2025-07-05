# lib/display_manager.py

import time
from machine import Pin, I2C
import ssd1306
import logger

class DisplayManager:
    def __init__(self,
                 scl_pin=9,
                 sda_pin=8,
                 width=128,
                 height=64,
                 i2c_freq=400000,
                 i2c_addr=0x3C):
        """
        Initialize I2C and SSD1306. If no device is found,
        oled is set to None and drawing calls become no-ops.
        """
        self.oled = None
        self.width = width
        self.height = height

        try:
            # Set up I2C bus
            self.scl = Pin(scl_pin)
            self.sda = Pin(sda_pin)
            self.i2c = I2C(0, scl=self.scl, sda=self.sda, freq=i2c_freq)
            devices = self.i2c.scan()
            logger.debug(f"I2C devices found: {devices}")

            if i2c_addr not in devices:
                raise OSError(f"SSD1306 not at address 0x{i2c_addr:02X}")

            # Initialize OLED
            self.oled = ssd1306.SSD1306_I2C(width, height, self.i2c, addr=i2c_addr)
            self.clear()
            logger.info("SSD1306 initialized successfully")
        except Exception as e:
            logger.error(f"SSD1306 init failed: {e}. Display disabled.")

    def clear(self):
        if not self.oled:
            return
        self.oled.fill(0)
        self.oled.show()

    def draw_sensor_matrix(self, matrix):
        if not self.oled:
            return
        self.oled.fill(0)
        max_val = 4095
        cell = 7
        cols = len(matrix)
        rows = len(matrix[0]) if cols else 0
        x_off = (self.width - cols * cell) // 2
        y_off = (self.height - rows * cell) // 2

        for c in range(cols):
            for r in range(rows):
                v = matrix[c][r]
                x = x_off + c * cell
                y = y_off + r * cell
                if v < 200:
                    continue
                elif v < 1000:
                    self.oled.pixel(x + 3, y + 3, 1)
                elif v < 2000:
                    self.oled.fill_rect(x + 2, y + 2, 3, 3, 1)
                elif v < 3000:
                    self.oled.fill_rect(x + 1, y + 1, 5, 5, 1)
                else:
                    self.oled.fill_rect(x, y, cell, cell, 1)

        self.oled.show()

    def update(self, state):
        if not self.oled:
            return
        self.oled.fill(0)
        line = 0

        mode = state.get('mode', '')
        if mode:
            self.oled.text(f"Mode: {mode}", 0, line * 8)
            line += 1

        menu_items = state.get('menu_items')
        sel = state.get('current_selection', 0)
        if menu_items:
            for idx, item in enumerate(menu_items):
                prefix = '>' if idx == sel else ' '
                self.oled.text(f"{prefix}{item}", 0, line * 8)
                line += 1

        self.oled.show()
