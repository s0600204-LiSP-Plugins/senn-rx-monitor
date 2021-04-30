# -*- coding: utf-8 -*-
#
# This file is a derivation of work on - and as such shares the same
# licence as - Linux Show Player
#
# Linux Show Player:
#   Copyright 2012-2021 Francesco Ceruti <ceppofrancy@gmail.com>
#
# This file:
#   Copyright 2021 s0600204
#
# Linux Show Player is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Linux Show Player is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Linux Show Player.  If not, see <http://www.gnu.org/licenses/>.

# pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QPushButton, QSizePolicy, QVBoxLayout

from lisp.plugins import get_plugin
from lisp.ui.icons import IconTheme
from lisp.ui.ui_utils import translate

from .mic_info_widget_container import MicInfoWidgetContainer

class MicInfoDialog(QDialog):

    def __init__(self, server, **kwargs):
        super().__init__(**kwargs)

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(4, 4, 4, 4)

        # Set flags so we get the min & max buttons
        # (and so they actually function)
        flags = self.windowFlags()
        flags ^= Qt.Dialog
        flags |= Qt.WindowMinMaxButtonsHint
        self.setWindowFlags(flags)

        self._container = MicInfoWidgetContainer(server)
        self._container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.layout().addWidget(self._container)

        self._discover_button = QPushButton()
        self._discover_button.setIcon(IconTheme.get('system-search'))
        self._discover_button.clicked.connect(get_plugin('SennRxMonitor').discover)

        self._buttons = QDialogButtonBox()
        self._buttons.addButton(self._discover_button, QDialogButtonBox.ActionRole)
        self._buttons.addButton(QDialogButtonBox.Close)
        self._buttons.rejected.connect(self.reject)
        self.layout().addWidget(self._buttons)

        self.retranslateUi()

    def count(self):
        return self._container.count()

    def minimumSizeHint(self):
        return self._container.minimumSizeHint()

    def retranslateUi(self):
        self.setWindowTitle(translate('senn_rx_monitor', 'Mic Info'))
        self._discover_button.setText(translate('senn_rx_monitor', 'Network Discover'))
