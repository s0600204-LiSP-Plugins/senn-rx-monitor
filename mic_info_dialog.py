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
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import QAction, QDialog, QDialogButtonBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMenu, QVBoxLayout

from lisp.plugins import get_plugin

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

        # Set flags so we get the min & max buttons
        # (and so they actually function)
        flags = self.windowFlags()
        flags ^= Qt.Dialog
        flags |= Qt.WindowMinMaxButtonsHint
        self.setWindowFlags(flags)

        self._add_dialog = None
        self._listener = listener
        self._menu = QMenu(self)
        self._size_hint = QSize(640, 256)
        self._widgets = []
        self.mouse_over_widget = None

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.make_push_request)
        self._timer.setInterval(UPDATE_DURATION * 1000)

        self.finished.connect(self._timer.stop)

    def _create_menu_action(self, caption, slot):
        new_action = QAction(caption, parent=self._menu)
        new_action.triggered.connect(slot)
        self._menu.addAction(new_action)

    def _create_menu_subheader(self, caption):
        new_action = QAction(caption, parent=self._menu)
        new_action.setEnabled(False)
        font = new_action.font()
        font.setBold(True)
        new_action.setFont(font)
        self._menu.addAction(new_action)

    def add_receiver(self):
        if not self._add_dialog:
            self._add_dialog = AddReceiverDialog(parent=self)

        if self._add_dialog.exec() == QDialog.Accepted:
            self.append_widget(self._add_dialog.ip())

    def append_widget(self, ip):
        new_widget = MicInfoWidget(ip)
        self.layout().addWidget(new_widget)
        self._listener.register(new_widget.ip(), new_widget.handle)
        new_widget.config_request.connect(self.make_config_update_request)
        self._widgets.append(new_widget)
        get_plugin('SennRxMonitor').append_rx(ip)

    def check_exists(self, ip):
        for widget in self._widgets:
            if widget.ip() == ip:
                return True
        return False

    def count(self):
        return len(self._widgets)

    def contextMenuEvent(self, event):
        self._menu.clear()

        if self.mouse_over_widget and isinstance(self.mouse_over_widget, MicInfoWidget):
            self._create_menu_subheader(self.mouse_over_widget.ip())
            self._create_menu_action('Remove Receiver', self.mouse_over_widget.delete_self)
            self._menu.addSeparator()

        self._create_menu_action('Add Receiver', self.add_receiver)
        self._menu.popup(event.globalPos())

        self.mouse_over_widget = None

    def make_push_request(self):
        for widget in self._widgets:
            Transmit(widget.ip(), 'Push {} {} 0'.format(UPDATE_DURATION, UPDATE_FREQUENCY))

    def make_config_update_request(self, ip):
        Transmit(ip, 'Push 0 0 1')

    def minimumSizeHint(self):
        return self._size_hint

    def open(self):
        super().open()
        self._timer.start()
        self.make_push_request()

    def remove_widget(self, widget):
        self._listener.deregister(widget.ip())
        widget.config_request.disconnect()
        self.layout().removeWidget(widget)
        self._widgets.remove(widget)
        get_plugin('SennRxMonitor').remove_rx(widget.ip())
        widget.deleteLater()

    def sizeHint(self):
        return self._size_hint

class AddReceiverDialog(QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle('Add Receiver')
        self.setLayout(QFormLayout())

        self._label = QLabel()
        self._label.setAlignment(Qt.AlignHCenter)
        self._label.setText('Enter an IP address')
        self.layout().addRow(self._label)

        self._ip_text = QLineEdit()
        self._ip_text.setInputMask('000.000.000.000')
        self.layout().addRow('IP Address:', self._ip_text)

        self._buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Close)
        self._buttons.accepted.connect(self.validate)
        self._buttons.rejected.connect(self.reject)
        self.layout().addRow(self._buttons)

    def ip(self):
        return self._ip_text.text()

    def validate(self):
        if not self._ip_text.hasAcceptableInput():
            self._label.setText('Not a valid IP address')
            return

        text = self._ip_text.text()
        for part in text.split('.'):
            if not part or int(part) > 255:
                self._label.setText('Not a valid IP address')
                return

        if self.parent().check_exists(text):
            self._label.setText('Address already in use')
            return

        self.accept()
