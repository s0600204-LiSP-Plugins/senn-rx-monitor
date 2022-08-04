
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction

from mic_rx_monitor import APP_NAME
from mic_rx_monitor.i18n import translate
from .menu import ApplicationMenu


class FileMenu(ApplicationMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fullScreenAction = QAction(self)
        self.fullScreenAction.setCheckable(True)
        self.fullScreenAction.triggered.connect(self._window.setFullScreen)
        self.addAction(self.fullScreenAction)

        self.addSeparator()

        self.exitAction = QAction(self)
        self.exitAction.triggered.connect(self._window.close)
        self.addAction(self.exitAction)

    def retranslateUi(self):
        self.setTitle(translate("MainWindow", "&File"))

        self.fullScreenAction.setText(translate("MainWindow", "Full Screen"))
        self.fullScreenAction.setStatusTip(translate("MainWindow", "Toggle Full Screen"))
        if QKeySequence(QKeySequence.FullScreen).isEmpty():
            self.fullScreenAction.setShortcut("F11")
        else:
            self.fullScreenAction.setShortcut(QKeySequence.FullScreen)

        self.exitAction.setText(translate("MainWindow", "Exit"))
        self.exitAction.setStatusTip(translate("MainWindow", "Exit {}").format(APP_NAME))
        self.exitAction.setShortcut(QKeySequence.Quit)
