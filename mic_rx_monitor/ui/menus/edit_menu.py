
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction

from mic_rx_monitor.i18n import translate
from .menu import ApplicationMenu


class EditMenu(ApplicationMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.actionManualAdd = QAction(self)
        self.actionManualAdd.triggered.connect(self._window.centralWidget().add_receiver)
        self.addAction(self.actionManualAdd)

        self.addSeparator()

        self.actionDiscoverMCP = QAction(self)
        self.actionDiscoverMCP.triggered.connect(self._application.core.discover)
        self.addAction(self.actionDiscoverMCP)

    def retranslateUi(self):
        self.setTitle(translate("MainWindow", "&Edit"))

        self.actionManualAdd.setText(translate("MainWindow", "Add Receiver by IP"))
        self.actionManualAdd.setShortcut(QKeySequence.New)

        self.actionDiscoverMCP.setText(translate("MainWindow", "Discover Sennheiser Receivers (MCP)"))
        self.actionDiscoverMCP.setShortcut("CTRL+SHIFT+R")
