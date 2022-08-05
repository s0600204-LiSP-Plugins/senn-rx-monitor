
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction, QMessageBox

from mic_rx_monitor import __name__ as APP_NAME
from mic_rx_monitor.i18n import translate
from .menu import ApplicationMenu


class FileMenu(ApplicationMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.resetAction = QAction(self)
        self.resetAction.triggered.connect(self.requestResetConfirmation)
        self.addAction(self.resetAction)

        self.addSeparator()

        self.fullScreenAction = QAction(self)
        self.fullScreenAction.setCheckable(True)
        self.fullScreenAction.triggered.connect(self._window.setFullScreen)
        self.addAction(self.fullScreenAction)

        self.addSeparator()

        self.exitAction = QAction(self)
        self.exitAction.triggered.connect(self._window.close)
        self.addAction(self.exitAction)

    def requestResetConfirmation(self):
        def reset():
            self._application.core.reset()
            self._window.showStatusTip(translate("mic_rx_monitor", "Removed all receivers"))

        confirmationDialog = QMessageBox(
            QMessageBox.Warning,
            translate("mic_rx_monitor", "Confirm reset"),
            translate("mic_rx_monitor", "This will remove all receivers. This cannot be undone.\n\nContinue?"),
            QMessageBox.Yes | QMessageBox.No,
            parent=self)
        confirmationDialog.accepted.connect(reset)
        confirmationDialog.open()

    def retranslateUi(self):
        self.setTitle(translate("MainWindow", "&File"))

        self.resetAction.setText(translate("MainWindow", "Reset"))
        self.resetAction.setStatusTip(translate("MainWindow", "Remove all Receivers"))

        self.fullScreenAction.setText(translate("MainWindow", "Full Screen"))
        self.fullScreenAction.setStatusTip(translate("MainWindow", "Toggle Full Screen"))
        if QKeySequence(QKeySequence.FullScreen).isEmpty():
            self.fullScreenAction.setShortcut("F11")
        else:
            self.fullScreenAction.setShortcut(QKeySequence.FullScreen)

        self.exitAction.setText(translate("MainWindow", "Exit"))
        self.exitAction.setStatusTip(translate("MainWindow", "Exit {}").format(APP_NAME))
        self.exitAction.setShortcut(QKeySequence.Quit)
