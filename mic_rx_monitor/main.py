
import signal
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from . import APP_NAME
from .application import Application

def main():
    # Create the QApplication
    qt_app = QApplication(sys.argv)
    qt_app.setApplicationName(APP_NAME)
    qt_app.setQuitOnLastWindowClosed(True)

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
