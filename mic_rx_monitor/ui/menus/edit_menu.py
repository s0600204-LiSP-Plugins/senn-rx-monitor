
from qtpy.QtGui import QKeySequence
from qtpy.QtWidgets import QAction

from mic_rx_monitor.i18n import translate
from .menu import ApplicationMenu


class EditMenu(ApplicationMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._actions['addManually'] = QAction(self)
        self._actions['addManually'].triggered.connect(self._window.centralWidget().add_receiver)
        self.addAction(self._actions['addManually'])

        self.addSeparator()

        self._actions['discoverMCP'] = QAction(self)
        self._actions['discoverMCP'].triggered.connect(self._application.core.discover)
        self.addAction(self._actions['discoverMCP'])

    def retranslateUi(self):
        self.setTitle(translate("MainWindow", "&Edit"))

        self._actions['addManually'].setText(
            translate("mic_rx_monitor", "Add Receiver"))
        self._actions['addManually'].setStatusTip(
            translate("mic_rx_monitor", "Manually add a receiver by IP"))
        self._actions['addManually'].setShortcut(QKeySequence.New)

        self._actions['discoverMCP'].setText(
            translate("mic_rx_monitor", "Discover MCP Receivers"))
        self._actions['discoverMCP'].setStatusTip(
            translate(
                "mic_rx_monitor",
                "Discover receivers available via Sennheiser's 'Media Control Protocol'"))
        self._actions['discoverMCP'].setShortcut("CTRL+SHIFT+R")
