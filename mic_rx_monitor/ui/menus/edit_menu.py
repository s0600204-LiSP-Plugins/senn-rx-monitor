
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

        self.actionManualAdd.setText(translate("mic_rx_monitor", "Add Receiver"))
        self.actionManualAdd.setStatusTip(
            translate("mic_rx_monitor", "Manually add a receiver by IP"))
        self.actionManualAdd.setShortcut(QKeySequence.New)

        self.actionDiscoverMCP.setText(translate("mic_rx_monitor", "Discover MCP Receivers"))
        self.actionDiscoverMCP.setStatusTip(
            translate("mic_rx_monitor", "Discover receivers available via Sennheiser's 'Media Control Protocol'"))
        self.actionDiscoverMCP.setShortcut("CTRL+SHIFT+R")
