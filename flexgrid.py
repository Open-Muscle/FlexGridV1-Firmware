# flexgrid.py

import uasyncio as asyncio
import uos
import logger

from settings_manager import SettingsManager
from sensor_matrix    import SensorMatrix
from display_manager  import DisplayManager
from menu_manager     import MenuManager
from network_manager  import NetworkManager

async def sensor_loop(sensor_matrix, network, display):
    while True:
        matrix = sensor_matrix.scan_matrix()
        logger.debug(f"Scanned[0:2]: {matrix[0:2]}")
        await network.send_udp(matrix)
        display.draw_sensor_matrix(matrix)
        await asyncio.sleep(0.1)

async def display_loop(display, menu):
    while True:
        state = menu.get_state()
        logger.debug(f"Display state: {state}")
        display.update(state)
        await asyncio.sleep(0.25)

async def menu_loop(menu):
    while True:
        logger.debug("Polling buttons")
        menu.check_buttons()
        await asyncio.sleep(0.05)

async def main():
    logger.info("FlexGrid startup")

    # Ensure config directory exists
    try:
        uos.stat('config')
    except OSError:
        logger.warn("No config folder—creating it")
        uos.mkdir('config')

    # Load settings (creates file if missing)
    settings = SettingsManager.load()
    logger.info(f"Loaded settings: {settings}")

    # Initialize modules
    display       = DisplayManager()
    sensor_matrix = SensorMatrix()
    network       = NetworkManager(settings)
    menu          = MenuManager(display, network)

    # Connect Wi-Fi & prepare UDP
    try:
        logger.info("Connecting network…")
        await network.connect()
        logger.info("Network connected")
    except Exception as e:
        logger.error(f"Network error: {e}")

    # Spawn background tasks
    logger.info("Starting async loops")
    asyncio.create_task(sensor_loop(sensor_matrix, network, display))
    asyncio.create_task(display_loop(display, menu))
    asyncio.create_task(menu_loop(menu))

    # Keep alive
    while True:
        await asyncio.sleep(1)
