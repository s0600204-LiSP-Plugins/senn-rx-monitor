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
from PyQt5.QtCore import QLine, QSize, QTimer
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QAction, QDialog, QMenu, QWidget

from lisp.plugins import get_plugin

from ..server import Transmit
from .add_receiver_dialog import AddReceiverDialog
from .qflowlayout import QFlowLayout
from .widgets.drag import DRAG_MAGIC
from .widgets.mic_info import MicInfoWidget

UPDATE_DURATION = 1 # seconds
UPDATE_FREQUENCY = 100 # milliseconds


class MicInfoWidgetContainer(QWidget):

    def __init__(self, listener):
        super().__init__()
        self.setLayout(QFlowLayout())
        self._size_hint = QSize(1025, 300)

        self._add_dialog = None
        self._listener = listener
        self._menu = QMenu(self)
        self.mouse_over_widget = None

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.make_push_request)
        self._timer.setInterval(UPDATE_DURATION * 1000)

        self.setAcceptDrops(True)
        self._dragDropIndex = None
        self._dragDropLine = None
        self._dragDropLineColor = QColor(160, 160, 160)

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
        get_plugin('SennRxMonitor').append_rx(ip)

    def check_exists(self, ip):
        for item in self.layout().children():
            if item.widget().ip() == ip:
                return True
        return False

    def count(self):
        return self.layout().count()

    def contextMenuEvent(self, event):
        self._menu.clear()

        if self.mouse_over_widget and isinstance(self.mouse_over_widget, MicInfoWidget):
            self._create_menu_subheader(self.mouse_over_widget.ip())
            self._create_menu_action('Remove Receiver', self.mouse_over_widget.delete_self)
            self._menu.addSeparator()

        self._create_menu_action('Add Receiver', self.add_receiver)
        self._menu.popup(event.globalPos())

        self.mouse_over_widget = None

    def dragEnterEvent(self, event):
        if event.mimeData().text() == DRAG_MAGIC:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        pos = event.pos()
        child = self.childAt(pos)
        if not child:
            return

        if not isinstance(child, MicInfoWidget):
            child = child.parent()

        self._dragDropIndex = self.layout().indexOf(child)
        rect = child.rect()
        line = QLine(
            child.mapToParent(rect.topRight()),
            child.mapToParent(rect.bottomRight())
        )
        line.translate(self.layout().horizontalSpacing() / 3 * 2, 0)
        self._dragDropLine = line
        self.update()

    def dropEvent(self, event):
        dropped = event.source().parent()
        new_index = self.layout().moveWidget(dropped, self._dragDropIndex)
        self._dragDropLine = None
        self._dragDropIndex = None
        get_plugin('SennRxMonitor').move_rx(dropped.ip(), new_index)

    def make_push_request(self):
        for item in self.layout().children():
            Transmit(item.widget().ip(), 'Push {} {} 0'.format(UPDATE_DURATION, UPDATE_FREQUENCY))

    def make_config_update_request(self, ip):
        Transmit(ip, 'Push 0 0 1')

    def minimumSize(self):
        return self.layout().minimumSize()

    def minimumSizeHint(self):
        return self._size_hint

    def paintEvent(self, _):
        if self._dragDropLine:
            painter = QPainter()
            painter.begin(self)
            painter.setPen(self._dragDropLineColor)
            painter.drawLine(self._dragDropLine)
            painter.end()

    def remove_widget(self, widget):
        self._listener.deregister(widget.ip())
        widget.config_request.disconnect()
        self.layout().removeWidget(widget)
        get_plugin('SennRxMonitor').remove_rx(widget.ip())
        widget.deleteLater()

    def reset(self):
        item = self.layout().takeAt(0)
        while item:
            self.remove_widget(item.widget())
            item = self.layout().takeAt(0)

    def start_timers(self):
        self._timer.start()
        self.make_push_request()

    def stop_timers(self):
        self._timer.stop()
