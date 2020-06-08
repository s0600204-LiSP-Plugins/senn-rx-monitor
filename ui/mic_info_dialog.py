# -*- coding: utf-8 -*-
#
# This file is a derivation of work on - and as such shares the same
# licence as - Linux Show Player
#
# Linux Show Player:
#   Copyright 2012-2020 Francesco Ceruti <ceppofrancy@gmail.com>
#
# This file:
#   Copyright 2020 s0600204
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
from PyQt5.QtWidgets import QDialog, QSizePolicy, QVBoxLayout

from .mic_info_widget_container import MicInfoWidgetContainer

class MicInfoDialog(QDialog):

    def __init__(self, listener, **kwargs):
        super().__init__(**kwargs)

        self.setWindowTitle('Mic Info')
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        # Set flags so we get the min & max buttons
        # (and so they actually function)
        flags = self.windowFlags()
        flags ^= Qt.Dialog
        flags |= Qt.WindowMinMaxButtonsHint
        self.setWindowFlags(flags)

        self._container = MicInfoWidgetContainer(listener)
        self.finished.connect(self._container.stop_timers)
        self._container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.layout().addWidget(self._container)

    def append_widget(self, ip):
        self._container.append_widget(ip)

    def count(self):
        return self._container.count()

    def minimumSizeHint(self):
        return self._container.minimumSizeHint()

    def open(self):
        super().open()
        self._container.start_timers()

    def reset(self):
        self._container.reset()
