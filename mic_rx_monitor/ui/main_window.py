
#from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QStatusBar,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)

from mic_rx_monitor import APP_NAME
from mic_rx_monitor.i18n import translate

from .menus.about_menu import AboutMenu
from .menus.edit_menu import EditMenu
from .menus.file_menu import FileMenu

class MainWindow(QMainWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setMinimumSize(640, 480)
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(QHBoxLayout())
        self.centralWidget().layout().setContentsMargins(4, 4, 4, 4)

        # Menu Bar
        self.menubar = QMenuBar(self)

        self.menuFile = FileMenu(self)
        self.menuEdit = EditMenu(self)
        self.menuAbout = AboutMenu(self)

        self.menubar.addMenu(self.menuFile)
        self.menubar.addMenu(self.menuEdit)
        self.menubar.addMenu(self.menuAbout)
        self.setMenuBar(self.menubar)

        # Status Bar
        self.setStatusBar(QStatusBar(self))

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(APP_NAME)

        # Menus
        self.menuFile.retranslateUi()
        self.menuEdit.retranslateUi()
        self.menuAbout.retranslateUi()
