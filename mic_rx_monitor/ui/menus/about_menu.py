
from PyQt5.QtWidgets import (
    QAction,
    qApp,
)

from mic_rx_monitor.i18n import translate
from .menu import ApplicationMenu


class AboutMenu(ApplicationMenu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._actions['aboutQt'] = QAction(self)
        self._actions['aboutQt'].triggered.connect(qApp.aboutQt)
        self.addAction(self._actions['aboutQt'])

    def retranslateUi(self):
        self.setTitle(translate("MainWindow", "&About"))

        self._actions['aboutQt'].setText(translate("MainWindow", "About Qt"))
