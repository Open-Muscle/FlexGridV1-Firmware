# lib/network_manager.py

import network
import socket
import uasyncio as asyncio
import ujson
import logger

class NetworkManager:
    def __init__(self, settings):
        # Expect settings dict with keys: wifi_ssid, wifi_password, udp_target_ip, udp_port
        self.ssid = settings.get("wifi_ssid", "").strip()
        self.password = settings.get("wifi_password", "").strip()
        self.udp_ip = settings.get("udp_target_ip", "255.255.255.255")
        self.udp_port = settings.get("udp_port", 3141)

        # Wi-Fi station interface
        self.sta = network.WLAN(network.STA_IF)
        self.sock = None

    async def connect(self):
        """Activate station interface and join the AP (unless no SSID is configured)."""
        if not self.ssid:
            logger.warn("No Wi-Fi SSID configured; skipping connection")
            return

        if not self.sta.active():
            self.sta.active(True)

        if not self.sta.isconnected():
            logger.info(f"Connecting to Wi-Fi SSID='{self.ssid}'…")
            self.sta.connect(self.ssid, self.password)
            # Wait up to ~20 seconds
            for _ in range(20):
                if self.sta.isconnected():
                    break
                await asyncio.sleep(1)

            if not self.sta.isconnected():
                raise RuntimeError("Wi-Fi connection failed")
        logger.info("Wi-Fi connected, IP: " + self.sta.ifconfig()[0])

        # Set up a non-blocking UDP socket
        if not self.sock:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setblocking(False)

    async def send_udp(self, matrix):
        """Serialize the matrix and send as a JSON UDP packet."""
        if not self.sock:
            return

        try:
            payload = ujson.dumps(matrix)
            self.sock.sendto(payload, (self.udp_ip, self.udp_port))
        except Exception as e:
            logger.error("UDP send error: " + str(e))
