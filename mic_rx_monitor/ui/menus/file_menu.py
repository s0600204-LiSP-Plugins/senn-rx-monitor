
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction, QMessageBox

from mic_rx_monitor import __app_name__
from mic_rx_monitor.i18n import translate
from .menu import ApplicationMenu


class FileMenu(ApplicationMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._actions['reset'] = QAction(self)
        self._actions['reset'].triggered.connect(self.request_reset_confirmation)
        self.addAction(self._actions['reset'])

        self.addSeparator()

        self._actions['fullscreen'] = QAction(self)
        self._actions['fullscreen'].setCheckable(True)
        self._actions['fullscreen'].triggered.connect(self._window.set_fullscreen)
        self.addAction(self._actions['fullscreen'])

        self.addSeparator()

        self._actions['exit'] = QAction(self)
        self._actions['exit'].triggered.connect(self._window.close)
        self.addAction(self._actions['exit'])

    def request_reset_confirmation(self):
        def reset():
            self._application.core.reset()
            self._window.show_status_message(translate("mic_rx_monitor", "Removed all receivers"))

        confirmation_dialog = QMessageBox(
            QMessageBox.Warning,
            translate("mic_rx_monitor", "Confirm reset"),
            translate(
                "mic_rx_monitor",
                "This will remove all receivers. This cannot be undone.\n\nContinue?"),
            QMessageBox.Yes | QMessageBox.No,
            parent=self)
        confirmation_dialog.accepted.connect(reset)
        confirmation_dialog.open()

    def retranslateUi(self):
        self.setTitle(translate("MainWindow", "&File"))

        self._actions['reset'].setText(translate("MainWindow", "Reset"))
        self._actions['reset'].setStatusTip(translate("MainWindow", "Remove all Receivers"))

        self._actions['fullscreen'].setText(translate("MainWindow", "Full Screen"))
        self._actions['fullscreen'].setStatusTip(translate("MainWindow", "Toggle Full Screen"))
        if QKeySequence(QKeySequence.FullScreen).isEmpty():
            self._actions['fullscreen'].setShortcut("F11")
        else:
            self._actions['fullscreen'].setShortcut(QKeySequence.FullScreen)

        self._actions['exit'].setText(translate("MainWindow", "Exit"))
        self._actions['exit'].setStatusTip(translate("MainWindow", "Exit {}").format(__app_name__))
        self._actions['exit'].setShortcut(QKeySequence.Quit)
