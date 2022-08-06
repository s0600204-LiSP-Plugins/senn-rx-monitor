
from .core import MicMonitorCore
from .file_io import (
    load_config_file,
    save_config_file,
)
from .i18n import translate
from .ui.main_window import MainWindow


class Application:

    def __init__(self):
        self._monitor_core = MicMonitorCore()
        self._mainwindow = MainWindow(self)

        self._config = None
        self.load_config()

        self._monitor_core.list_updated.connect(self.save_rx_list)

    @property
    def core(self):
        return self._monitor_core

    def start(self):
        self._mainwindow.show()

    def load_config(self):
        self._config = load_config_file()
        if not self._config:
            self._mainwindow.showStatusTip(
                translate("mic_rx_monitor", "No valid configuration found"))
            return

        self._monitor_core.load(self._config['rx'])
        self._mainwindow.showStatusTip(
            translate("mic_rx_monitor", "Configuration restored"))

    def save_rx_list(self, rx_list):
        self._config['rx'] = rx_list
        save_config_file(self._config)
