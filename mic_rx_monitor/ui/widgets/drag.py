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

from qtpy.QtCore import QMimeData, Qt
from qtpy.QtGui import QDrag, QPainter, QPainterPath
from qtpy.QtWidgets import QWidget

from ..colors import Colors

DRAG_MAGIC = 'RF_Drag&Drop'


class DragWidget(QWidget):

    gap = 2

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        height = int(self.gap * 3.5)
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)

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
            painter.setPen(Colors.line(self, Colors.State.HOVER))
        else:
            painter.setPen(Colors.line(self, Colors.State.NORMAL))

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
