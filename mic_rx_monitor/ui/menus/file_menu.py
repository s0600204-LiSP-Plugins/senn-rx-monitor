
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QMenu,
    QAction,
)

from ...i18n import translate

class FileMenu(QMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.exitAction = QAction(self)
        self.exitAction.triggered.connect(self.__mainwindow().close)

        self.addAction(self.exitAction)

    def __mainwindow(self):
        candidate = self.parent()
        while not isinstance(candidate, QMainWindow):
            if candidate is None:
                return None
            candidate = candidate.parent()
        return candidate

    def retranslateUi(self):
        self.setTitle(translate("MainWindow", "&File"))

        # ~ self.fullScreenAction.setText(translate("MainWindow", "Full Screen"))
        # ~ self.fullScreenAction.setShortcut(QKeySequence.FullScreen)
        self.exitAction.setText(translate("MainWindow", "Exit"))
        self.exitAction.setShortcut(QKeySequence.Quit)
