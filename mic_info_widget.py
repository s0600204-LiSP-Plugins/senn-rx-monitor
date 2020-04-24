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
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget

from .meters import AFMeter, RFMeter


class MicInfoWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(100, 250)
        self.setMaximumWidth(150)

        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        #self.layout().setHorizontalSpacing(self.layout().horizontalSpacing() * 1.25)
        self.layout().setRowStretch(2, 1)

        self._label_name = QLabel()
        self._label_name.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self._label_name, 0, 0, 1, 2)

        self._label_freq = QLabel()
        self._label_freq.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self._label_freq, 1, 0, 1, 2)

        self._rf_meter = RFMeter()
        self.layout().addWidget(self._rf_meter, 2, 0)

        self._af_meter = AFMeter()
        self.layout().addWidget(self._af_meter, 2, 1)

    def set_name(self, name):
        self._label_name.setText(name)

    def set_freq(self, freq):
        self._label_freq.setText(freq)
