
from importlib.metadata import version
from os import path

from appdirs import AppDirs


_app_dirs = AppDirs(
    "MicRxMonitor"
)

def _split_vers(vers):
    vers = vers.split(".")
    for idx in range(3):
        vers[idx] = int(vers[idx])
    for idx in range(3, len(vers)):
        vers[idx:idx+1] = vers[idx].split("+")
    return tuple(vers)


__author__ = "s0600204"
__doc__ = "Monitoring of Sennheiser Radio Microphone Receivers"
__name__ = "Sennheiser RX Monitor"
__config_file__ = path.join(_app_dirs.user_config_dir, "config.yaml")
__version__ = version(path.split(path.dirname(__file__))[-1])
__version_info__ = _split_vers(__version__)
