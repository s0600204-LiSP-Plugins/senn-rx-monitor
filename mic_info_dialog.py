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
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout

from .mic_info_widget import MicInfoWidget
from .server import Transmit

UPDATE_DURATION = 1 # seconds
UPDATE_FREQUENCY = 100 # milliseconds

class MicInfoDialog(QDialog):

    def __init__(self, listener, **kwargs):
        super().__init__(**kwargs)

        self.setWindowTitle('Mic Info')
        self.setLayout(QHBoxLayout())
        self.layout().setAlignment(Qt.AlignLeft)

        self._listener = listener
        self._widgets = []

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.make_push_request)
        self._timer.setInterval(UPDATE_DURATION * 1000)

        self.finished.connect(self._timer.stop)

        self.append_widget('192.168.5.100')

    def append_widget(self, ip):
        new_widget = MicInfoWidget(ip)
        self.layout().addWidget(new_widget)
        self._listener.register(new_widget.ip(), new_widget.handle)
        new_widget.config_request.connect(self.make_config_update_request)
        self._widgets.append(new_widget)

    def make_push_request(self):
        for widget in self._widgets:
            Transmit(widget.ip(), 'Push {} {} 0'.format(UPDATE_DURATION, UPDATE_FREQUENCY))

    def make_config_update_request(self, ip):
        Transmit(ip, 'Push 0 0 1')

    def open(self):
        super().open()
        self._timer.start()
        self.make_push_request()
