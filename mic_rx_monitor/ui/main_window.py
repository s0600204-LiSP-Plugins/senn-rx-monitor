
#from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from mic_rx_monitor import APP_NAME
from mic_rx_monitor.i18n import translate

from .menus.about_menu import AboutMenu
from .menus.edit_menu import EditMenu
from .menus.file_menu import FileMenu
from .mic_info_widget_container import MicInfoWidgetContainer

class MainWindow(QMainWindow):

    STATUSBAR_MSG_DURATION = 3000 # ms

    def __init__(self, application, **kwargs):
        super().__init__(**kwargs)

        self.setMinimumSize(640, 480)
        self.setCentralWidget(MicInfoWidgetContainer(application.core))
        self.centralWidget().layout().setContentsMargins(4, 4, 4, 4)

        self._application = application

        # Menu Bar
        self.menubar = QMenuBar(self)

        self.menuFile = FileMenu(self)
        self.menuEdit = EditMenu(self)
        self.menuAbout = AboutMenu(self)

        self.menubar.addMenu(self.menuFile)
        self.menubar.addMenu(self.menuEdit)
        self.menubar.addMenu(self.menuAbout)
        self.setMenuBar(self.menubar)

        # Listeners to show messages on Status Bar
        application.core.rx_added.connect(self.on_rx_added)
        application.core.rx_moved.connect(self.on_rx_moved)
        application.core.rx_removed.connect(self.on_rx_removed)

        self.retranslateUi()

    def on_rx_added(self, ip, _):
        self.showStatusTip(
            translate("mic_rx_monitor", "Added new receiver at {ip}").format(ip=ip))

    def on_rx_moved(self, ip, *_):
        self.showStatusTip(
            translate("mic_rx_monitor", "Moved receiver at {ip}").format(ip=ip))

    def on_rx_removed(self, ip):
        self.showStatusTip(
            translate("mic_rx_monitor", "Removed receiver at {ip}").format(ip=ip))

    def retranslateUi(self):
        self.setWindowTitle(APP_NAME)

        # Menus
        self.menuFile.retranslateUi()
        self.menuEdit.retranslateUi()
        self.menuAbout.retranslateUi()

    def showStatusTip(self, message):
        self.statusBar().showMessage(
            message,
            self.STATUSBAR_MSG_DURATION
        )
