
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QAction,
    QMenu,
    QMenuBar,
    qApp,
)

from ...i18n import translate

class AboutMenu(QMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Actions
        self.actionAboutQt = QAction(self)
        self.actionAboutQt.triggered.connect(qApp.aboutQt)

        # Order of Options
        self.addAction(self.actionAboutQt)

    def retranslateUi(self):
        self.setTitle(translate("MainWindow", "&About"))

        # ~ self.actionAbout.setText(translate("MainWindow", "About"))
        self.actionAboutQt.setText(translate("MainWindow", "About Qt"))
