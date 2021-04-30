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
from PyQt5.QtCore import QMimeData, Qt
from PyQt5.QtGui import QColor, QDrag, QPainter, QPainterPath
from PyQt5.QtWidgets import QWidget

DRAG_MAGIC = 'RF_Drag&Drop'

class DragWidget(QWidget):

    gap = 2

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        height = self.gap * 2 + 3
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        self._segments = []

        self._border_color = QColor(80, 80, 80)
        self._hover_color = QColor(160, 160, 160)

    def mousePressEvent(self, event):
        # pylint: disable=invalid-name
        if event.button() != Qt.LeftButton:
            return

        mime_data = QMimeData()
        mime_data.setText(DRAG_MAGIC)

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(self.grab(self.parent().rect()))
        drag.exec_(Qt.MoveAction)

    def paintEvent(self, _):
        # pylint: disable=invalid-name
        width = self.width()

        painter = QPainter()
        painter.begin(self)

        if self.underMouse():
            painter.setPen(self._hover_color)
        else:
            painter.setPen(self._border_color)

        path = QPainterPath()
        path.moveTo(    0,      0)
        path.lineTo(width,      0)
        offset = self.gap + 1
        path.moveTo(    0, offset)
        path.lineTo(width, offset)
        offset = self.gap * 2 + 2
        path.moveTo(    0, offset)
        path.lineTo(width, offset)
        painter.drawPath(path)
        painter.end()
