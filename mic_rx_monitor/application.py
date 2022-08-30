
from .core import MicMonitorCore
from .file_io import (
    load_config_file,
    save_config_file,
)
from .i18n import translate
from .ui.main_window import MainWindow


class Application:

    def __init__(self, qt_app):
        self._qt_app = qt_app
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

        # Reposition in middle of screen
        screen_geometry = self._qt_app.primaryScreen().geometry()
        window_geometry = self._mainwindow.frameGeometry()
        self._mainwindow.move(
            int((screen_geometry.width() - window_geometry.width()) / 2 + screen_geometry.x()),
            int((screen_geometry.height() - window_geometry.height()) / 2 + screen_geometry.y()))

    def load_config(self):
        self._config = load_config_file()
        if not self._config:
            self._mainwindow.show_status_message(
                translate("mic_rx_monitor", "No valid configuration found"))
            return

        self._monitor_core.load(self._config['rx'])
        self._mainwindow.show_status_message(
            translate("mic_rx_monitor", "Configuration restored"))

    def save_rx_list(self, rx_list):
        self._config['rx'] = rx_list
        save_config_file(self._config)
