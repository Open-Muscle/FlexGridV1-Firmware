# lib/sensor_matrix.py

from machine import Pin, ADC
import time

class SensorMatrix:
    """
    Handles scanning a 16-column × N-row sensor matrix via a 4-bit MUX and multiple ADC inputs.
    Default is 16 columns and 4 rows (ADC channel pins 1–4).
    """

    def __init__(
        self,
        adc_pins=(1, 2, 3, 4),
        mux_pins=(5, 6, 7, 15),
        mux_en_pin=16,
        attenuation=ADC.ATTN_11DB,
        delay_us=100
    ):
        # Initialize MUX address pins
        self.S0 = Pin(mux_pins[0], Pin.OUT)
        self.S1 = Pin(mux_pins[1], Pin.OUT)
        self.S2 = Pin(mux_pins[2], Pin.OUT)
        self.S3 = Pin(mux_pins[3], Pin.OUT)
        self.mux_en = Pin(mux_en_pin, Pin.OUT)
        self.mux_en.value(0)      # LOW = enable MUX

        # Initialize ADC channels for each row
        self.adc = []
        for pin_num in adc_pins:
            adc = ADC(Pin(pin_num))
            adc.atten(attenuation)
            self.adc.append(adc)

        self.num_cols = 16
        self.num_rows = len(self.adc)
        self.delay_us = delay_us

    def _select_channel(self, channel):
        """Set the 4-bit address on the MUX for the given column (0–15)."""
        bits = [(channel >> i) & 1 for i in range(4)]
        self.S0.value(bits[0])
        self.S1.value(bits[1])
        self.S2.value(bits[2])
        self.S3.value(bits[3])

    def scan_matrix(self):
        """
        Scans all columns and returns a list of lists:
        [
          [col0_row0, col0_row1, ..., col0_rowN],
          [col1_row0, ...],
          ...
          [col15_rowN]
        ]
        """
        matrix = [[0] * self.num_rows for _ in range(self.num_cols)]

        for col in range(self.num_cols):
            self._select_channel(col)
            time.sleep_us(self.delay_us)  # allow signal to settle
            for row in range(self.num_rows):
                matrix[col][row] = self.adc[row].read()

        return matrix
