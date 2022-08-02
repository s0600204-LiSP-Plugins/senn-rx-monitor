# This file is a derivation of work on - and as such shares the same
# licence as - Linux Show Player
#
# Linux Show Player:
#   Copyright 2012-2022 Francesco Ceruti <ceppofrancy@gmail.com>
#
# This file:
#   Copyright 2022 s0600204
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
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget

from lisp.core.signal import Connection

from ..colors import Colors
from .battery_indicator import BatteryIndicator
from .drag import DragWidget
from .meters import AFMeter, RFMeter
from .status_indicator import StatusIndicator


class MicInfoWidget(QWidget):

    def __init__(self, worker, monitor_core):
        super().__init__()

        self._config_num = -1
        self._worker = worker
        self._core = monitor_core

        self.setMinimumSize(120, 300)
        self.setMaximumWidth(120)

        self.setLayout(QGridLayout())
        margin = self.layout().horizontalSpacing()
        self.layout().setContentsMargins(margin, margin, margin, margin)
        self.layout().setRowStretch(3, 1)

        self._drag_widget = DragWidget()
        self.layout().addWidget(self._drag_widget, 0, 0, 1, 2)

        self._label_name = QLabel()
        self._label_name.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self._label_name, 1, 0, 1, 2)

        self._label_freq = QLabel()
        self._label_freq.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self._label_freq, 2, 0, 1, 2)

        self._rf_meter = RFMeter()
        self.layout().addWidget(self._rf_meter, 3, 0)
        self._rf_levels = [[], []]

        self._af_meter = AFMeter()
        self.layout().addWidget(self._af_meter, 3, 1)

        self._battery_meter = BatteryIndicator()
        self.layout().addWidget(self._battery_meter, 4, 0, 1, 2)

        self._status_indicator = StatusIndicator()
        self.layout().addWidget(self._status_indicator, 5, 0, 1, 2)

        self.reset()

        # We use Connection.QtQueued as the signals are emitted on the server/listener thread
        # and we need to run the connected methods on the main event loop thread.
        self._worker.lost_connection.connect(self.reset, Connection.QtQueued)
        self._worker.updated_af_level.connect(self.set_af, Connection.QtQueued)
        self._worker.updated_battery_status.connect(self.update_battery_status, Connection.QtQueued)
        self._worker.updated_config_num.connect(self.check_config, Connection.QtQueued)
        self._worker.updated_frequency.connect(self.set_freq, Connection.QtQueued)
        self._worker.updated_name.connect(self.set_name, Connection.QtQueued)
        self._worker.updated_rf.connect(self.set_rf, Connection.QtQueued)
        self._worker.updated_rf_levels.connect(self.parse_rf, Connection.QtQueued)
        self._worker.updated_status.connect(self.update_status, Connection.QtQueued)
        self._worker.updated_squelch.connect(self.set_squelch, Connection.QtQueued)

    def check_config(self, config_num):
        if config_num == self._config_num:
            return
        self._config_num = config_num
        self._worker.request_config()

    def clear(self):
        self._rf_meter.reset()
        self._af_meter.reset()
        self._rf_levels = [[], []]

    @property
    def is_online(self):
        return self._config_num != -1

    def contextMenuEvent(self, event):
        self.parent().mouse_over_widget = self
        self.parent().contextMenuEvent(event)

    def delete_self(self):
        self._core.remove_rx(self.ip())

    def ip(self):
        return self._worker.ip()

    def paintEvent(self, _):
        # pylint: disable=invalid-name
        painter = QPainter()
        painter.begin(self)
        painter.setPen(Colors.line(self))
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
        painter.end()

    def parse_rf(self, level, peak):
        self._rf_levels[0].append(level)
        self._rf_levels[1].append(peak)

    def rename_self(self):
        new_name = self.parent().request_new_receiver_name(self._label_name.text())
        if new_name:
            self._worker.send_rename_request(new_name)

    def reset(self):
        self.clear()
        self._label_name.setText("-")
        self._label_freq.setText("-")
        self._battery_meter.setFilled("?")
        self._status_indicator.reset()
        self._config_num = -1

    def set_af(self, level, peak):
        self._af_meter.plot([level], [peak])

    def set_freq(self, freq):
        self._label_freq.setText(f"{freq[0:3]}.{freq[3:6]} MHz")

    def set_name(self, name):
        self._label_name.setText(name)

    def set_rf(self):
        self._rf_meter.plot(*self._rf_levels)
        self._rf_levels = [[], []]

    def set_squelch(self, squelch):
        self._rf_meter.setSquelch(squelch)

    def update_battery_status(self, status):
        self._battery_meter.setFilled(status)

    def update_status(self, statuses):
        self._status_indicator.setStatus(statuses)
