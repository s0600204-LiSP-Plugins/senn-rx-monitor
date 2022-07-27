
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QMenuBar,
    QMenu,
    QAction,
)

from ...i18n import translate

class EditMenu(QMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def retranslateUi(self):
        self.setTitle(translate("MainWindow", "&Edit"))

        # @todo: Add options here
