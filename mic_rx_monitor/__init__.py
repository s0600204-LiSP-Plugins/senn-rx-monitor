
from appdirs import AppDirs
from os import path


app_dirs = AppDirs(
    "MicRxMonitor"
)


# Application wide "constants"
APP_NAME = "Sennheiser RX Monitor"

APP_CONFIG_FILE = path.join(app_dirs.user_config_dir, "config.yaml")
