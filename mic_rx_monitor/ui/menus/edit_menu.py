
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction

from mic_rx_monitor.i18n import translate
from .menu import ApplicationMenu


class EditMenu(ApplicationMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def retranslateUi(self):
        self.setTitle(translate("MainWindow", "&Edit"))

        # @todo: Add options here
