
from .core import MicMonitorCore
from .ui.main_window import MainWindow

class Application:

    def __init__(self):
        self._monitor_core = MicMonitorCore()
        self._mainwindow = MainWindow(self)

    @property
    def core(self):
        return self._monitor_core

    def start(self):
        self._mainwindow.show()
