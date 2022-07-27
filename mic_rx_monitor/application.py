
from .ui.main_window import MainWindow

class Application:

    def __init__(self):
        self._mainwindow = MainWindow()

    def start(self):
        self._mainwindow.show()
