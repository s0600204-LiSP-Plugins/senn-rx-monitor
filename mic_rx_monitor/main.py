
from os import path
import signal
import sys

from qtpy.QtCore import QTimer
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QApplication

import qdarktheme

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

    custom = {
        "border": "#5a5a62",
        "foreground": "#d4d4e4",
        "background": "#1a1a1a",
        "primary": "#8a8af7",
    }
    qt_app.setPalette(qdarktheme.load_palette(custom_colors=custom))
    qt_app.setStyleSheet(qdarktheme.load_stylesheet(custom_colors=custom))

    qt_app.setWindowIcon(
        QIcon(f"{path.dirname(__file__)}/ui/icons/mic_rx_monitor.svg")
    )

    # Handle SIGTERM and SIGINT by quitting the QApplication
    def handle_quit_signal(*_):
        qt_app.quit()

    signal.signal(signal.SIGTERM, handle_quit_signal)
    signal.signal(signal.SIGINT, handle_quit_signal)

    # Initialize the application
    rx_app = Application(qt_app)

    # Run the application
    QTimer.singleShot(0, rx_app.start)
    exit_code = qt_app.exec() if hasattr(qt_app, "exec") else qt_app.exec_()

    # Cleanup
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
