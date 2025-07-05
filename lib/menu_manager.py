# menu_manager.py
from machine import Pin
import time

class MenuManager:
    def __init__(self, display, network,
                 select_pin=10, menu_pin=21,
                 debounce_ms=200):
        self.display = display
        self.network = network

        # Buttons (active LOW)
        self.select_btn = Pin(select_pin, Pin.IN, Pin.PULL_UP)
        self.menu_btn   = Pin(menu_pin,   Pin.IN, Pin.PULL_UP)
        self.debounce  = debounce_ms

        # Menu state
        self.menus = [
            ["Start Session", "Settings", "About"],
            ["Wi-Fi", "UDP Target", "Back"],
            ["Info", "Version", "Back"]
        ]
        self.current_menu = 0
        self.current_selection = 0

    def _debounced(self, pin):
        if pin.value() == 0:
            time.sleep_ms(self.debounce)
            while pin.value() == 0:
                pass
            return True
        return False

    def check_buttons(self):
        # Toggle between menus
        if self._debounced(self.menu_btn):
            self.current_menu = (self.current_menu + 1) % len(self.menus)
            self.current_selection = 0

        # Move selection or activate
        if self._debounced(self.select_btn):
            # Example: wrap selection
            self.current_selection = (self.current_selection + 1) % len(self.menus[self.current_menu])
            # TODO: add “enter” logic here for activating an item

    def get_state(self):
        """Return a dict for DisplayManager.update()."""
        return {
            "mode": f"Menu {self.current_menu}",
            "menu_items": self.menus[self.current_menu],
            "current_selection": self.current_selection
        }
