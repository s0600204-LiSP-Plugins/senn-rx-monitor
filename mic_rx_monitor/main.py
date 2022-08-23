
from os import path
import signal
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

import qdarkstyle

# Append vendored code to module path
# This is so we don't have to `try [...] except ImportError` code vendored from LiSP
sys.path.insert(1, path.join(path.dirname(__file__), '_vendor'))

# This must be placed below the `sys.path.insert()` above
# pylint: disable=wrong-import-position
from . import __app_name__
from .application import Application

def main():
    # Create the QApplication
    qt_app = QApplication(sys.argv)
    qt_app.setApplicationName(__app_name__)
    qt_app.setQuitOnLastWindowClosed(True)

    qt_app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    qt_app.setWindowIcon(
        QIcon(f"{path.dirname(__file__)}/ui/icons/mic_rx_monitor.svg")
    )

    # Handle SIGTERM and SIGINT by quitting the QApplication
    def handle_quit_signal(*_):
        qt_app.quit()

    signal.signal(signal.SIGTERM, handle_quit_signal)
    signal.signal(signal.SIGINT, handle_quit_signal)

    # Initialize the application
    rx_app = Application()

    # Run the application
    QTimer.singleShot(0, rx_app.start)
    exit_code = qt_app.exec()

    # Cleanup
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
