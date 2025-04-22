from configparser import ConfigParser

_CONFIG = None
CONFIG_PATH = "config.example.ini"

def get_config() -> dict:
    global _CONFIG
    if _CONFIG is not None:
        return _CONFIG
    config = ConfigParser()
    config.read(CONFIG_PATH)
    _CONFIG = config
    return config
