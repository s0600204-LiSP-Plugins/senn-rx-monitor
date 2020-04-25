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
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QColor, QPainter, QPainterPath
from PyQt5.QtWidgets import QWidget

class BatteryIndicator(QWidget):

    margin = 6

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.setMinimumHeight(28)
        self._segments = []
        self._filled = -1

        self._background_color = QColor(32, 32, 32)
        self._border_color = QColor(80, 80, 80)
        self._segment_border_color = self.palette().highlight().color()
        self._segment_border_low_color = QColor(250, 0, 0)
        self._segment_fill_brush = self.palette().highlight()

    def paintEvent(self, _):
        # pylint: disable=invalid-name
        height = self.height()
        width = self.width()

        painter = QPainter()
        painter.begin(self)

        painter.setBrush(self._background_color)
        painter.setPen(self._border_color)
        painter.drawRect(QRect(0, 0, width - 1, height - 1))

        if self._filled == -1:
            painter.drawText(0, 0, width, height, Qt.AlignCenter, "No Batt. Status")
            painter.end()
            return

        painter.setRenderHint(QPainter.Antialiasing, True)
        if self._filled == 0:
            painter.setPen(self._segment_border_low_color)
        else:
            painter.setPen(self._segment_border_color)

        for seg_num, segment in enumerate(self._segments):
            path = QPainterPath()
            for p_num, point in enumerate(segment):
                if p_num == 0:
                    path.moveTo(*point)
                else:
                    path.lineTo(*point)
            path.closeSubpath()
            if seg_num < self._filled:
                painter.setBrush(self._segment_fill_brush)
            else:
                painter.setBrush(self._background_color)
            painter.drawPath(path)

        painter.end()

    def resizeEvent(self, _):
        # pylint: disable=invalid-name
        self.updateSegments()

    def setFilled(self, value):
        # pylint: disable=invalid-name
        self._filled = {
            '100': 3,
            '70': 2,
            '30': 1,
            '0': 0,
            '?': -1,
        }.get(value)
        self.update()

    def updateSegments(self):
        # pylint: disable=invalid-name
        height = self.height() - self.margin * 2
        width = self.width() - self.margin * 2
        jut = height / 4
        gap = self.margin / 2
        seventh = (width - gap * 2) / 7

        def _apply_offset(segment, hoffset):
            for point in segment:
                point[0] += hoffset
                point[1] += self.margin

        # Determine the points to draw the following:
        # |‾‾/ /‾‾/ /‾|
        # |_/ /__/ /__|
        left_segment = [
            [0, 0],
            [seventh * 2 + jut - gap, 0],
            [seventh * 2 - jut - gap, height],
            [0, height]
        ]
        offset = self.margin
        _apply_offset(left_segment, self.margin)

        centre_segment = [
            [jut, 0],
            [seventh * 3 + jut - gap, 0],
            [seventh * 3 - jut - gap, height],
            [-jut, height]
        ]
        offset += seventh * 2 + gap
        _apply_offset(centre_segment, offset)

        right_segment = [
            [jut, 0],
            [seventh * 2, 0],
            [seventh * 2, height],
            [-jut, height]
        ]
        offset += seventh * 3 + gap
        _apply_offset(right_segment, offset)

        self._segments = [
            left_segment,
            centre_segment,
            right_segment,
        ]
