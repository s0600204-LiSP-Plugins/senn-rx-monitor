
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction

from mic_rx_monitor.i18n import translate
from .menu import ApplicationMenu


class FileMenu(ApplicationMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.exitAction = QAction(self)
        self.exitAction.triggered.connect(self._window.close)

        self.addAction(self.exitAction)

    def retranslateUi(self):
        self.setTitle(translate("MainWindow", "&File"))

        # ~ self.fullScreenAction.setText(translate("MainWindow", "Full Screen"))
        # ~ self.fullScreenAction.setShortcut(QKeySequence.FullScreen)
        self.exitAction.setText(translate("MainWindow", "Exit"))
        self.exitAction.setShortcut(QKeySequence.Quit)
