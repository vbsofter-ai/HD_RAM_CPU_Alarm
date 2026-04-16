import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "cpu_threshold": 90,
    "ram_threshold": 90,
    "disk_threshold": 90,
    "update_interval_ms": 1000,
    "notifications_enabled": True
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            # Merge with defaults in case of missing keys
            config = DEFAULT_CONFIG.copy()
            config.update(data)
            return config
    except Exception:
        return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
