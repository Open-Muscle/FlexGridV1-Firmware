# settings_manager.py

import json
import uos

class SettingsManager:
    # Define your default keys & values here
    DEFAULTS = {
        "wifi_ssid": "OpenMuscle",
        "wifi_password": "3141592653",
        "udp_target_ip": "192.168.1.49",
        "udp_port": 3141
    }

    @staticmethod
    def load():
        """Load existing settings or fall back to defaults."""
        try:
            with open('config/settings.json', 'r') as f:
                return json.load(f)
        except Exception:
            return SettingsManager.DEFAULTS.copy()

    @staticmethod
    def save(settings):
        """Save the given dict to config/settings.json, creating the folder if needed."""
        try:
            # Ensure the config directory exists
            try:
                uos.stat('config')
            except OSError:
                uos.mkdir('config')

            with open('config/settings.json', 'w') as f:
                json.dump(settings, f)
            return True
        except Exception as e:
            print("[ERR] Could not save settings:", e)
            return False
