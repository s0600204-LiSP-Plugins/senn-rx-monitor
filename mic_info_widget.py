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
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget

from lisp.core.decorators import async_function
from lisp.core.signal import Signal

from .battery_indicator import BatteryIndicator
from .meters import AFMeter, RFMeter


class MicInfoWidget(QWidget):

    config_request = Signal()

    def __init__(self, ip):
        super().__init__()

        self._config_num = -1
        self._ip = ip

        self._border_color = QColor(80, 80, 80)
        self.setMinimumSize(120, 250)
        self.setMaximumWidth(120)

        self.setLayout(QGridLayout())
        margin = self.layout().horizontalSpacing()
        self.layout().setContentsMargins(margin, margin, margin, margin)
        self.layout().setRowStretch(2, 1)

        self._label_name = QLabel()
        self._label_name.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self._label_name, 0, 0, 1, 2)

        self._label_freq = QLabel()
        self._label_freq.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self._label_freq, 1, 0, 1, 2)

        self._rf_meter = RFMeter()
        self.layout().addWidget(self._rf_meter, 2, 0)
        self._rf_levels = [[], []]

        self._af_meter = AFMeter()
        self.layout().addWidget(self._af_meter, 2, 1)

        self._battery_meter = BatteryIndicator()
        self.layout().addWidget(self._battery_meter, 3, 0, 1, 2)

        self.reset()

    def check_config(self, attrs):
        if attrs[0] == self._config_num:
            return
        self._config_num = attrs[0]
        self.config_request.emit(self._ip)

    def clear(self):
        self._rf_meter.reset()
        self._af_meter.reset()
        self._rf_levels = [[], []]

    def handle(self, command, attributes):
        handlers = {
            # Responses to specific commands
            'Name': lambda attrs: self._label_name.setText(attrs[0]),
            'Frequency': self.set_freq,
            #'Squelch'
            #'AfOut'
            #'Equalizer`
            #'Mute'

            # Cyclic Attributes.
            # These are always received in the same order, and are listed in that order.
            'RF1': self.parse_rf,
            'RF2': self.parse_rf,
            #'States'
            'RF': self.set_rf,
            'AF': self.set_af,
            'Bat': lambda attrs: self._battery_meter.setFilled(attrs[0]),
            #'Msg'
            'Config': self.check_config,
        }
        handlers.get(command, lambda _: None)(attributes)

    def ip(self):
        return self._ip

    def paintEvent(self, _):
        # pylint: disable=invalid-name
        painter = QPainter()
        painter.begin(self)
        painter.setPen(self._border_color)
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
        painter.end()

    def parse_rf(self, attrs):
        self._rf_levels[0].append(int(attrs[0]))
        self._rf_levels[1].append(int(attrs[1]))

    def reset(self):
        self.clear()
        self._label_name.setText("-")
        self._label_freq.setText("-")
        self._battery_meter.setFilled("?")

    @async_function
    def set_af(self, attrs):
        self._af_meter.plot([int(attrs[0])], [int(attrs[1])])

    def set_freq(self, attrs):
        freq = attrs[0]
        self._label_freq.setText("{}.{} MHz".format(freq[0:3], freq[3:6]))

    def set_name(self, name):
        self._label_name.setText(name)

    @async_function
    def set_rf(self, _):
        self._rf_meter.plot(*self._rf_levels)
        self._rf_levels = [[], []]
