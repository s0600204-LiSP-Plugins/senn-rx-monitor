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
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor, QPainter, QPainterPath
from PyQt5.QtWidgets import QWidget

class StatusIndicator(QWidget):

    margin = 6

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.setMinimumHeight(28)
        self._symbols = {}
        self._statuses = {
            'tx': -1,
            'rf': -1,
            'rx': -1,
        }

        self._background_color = QColor(32, 32, 32)
        self._error_color = QColor(255, 0, 0)
        self._ok_color = QColor(0, 160, 0)
        self._noinfo_color = QColor(80, 80, 80)

    def paintEvent(self, _):
        # pylint: disable=invalid-name
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setBrush(self._background_color)

        for name, symbol in self._symbols.items():

            if self._statuses[name] == -1:
                painter.setPen(self._noinfo_color)
            elif self._statuses[name] == 0:
                painter.setPen(self._ok_color)
            elif self._statuses[name] == 1:
                painter.setPen(self._error_color)

            path = QPainterPath()
            for point in symbol:
                if point[0] == 'l':
                    if point[3] == 'm':
                        path.moveTo(*point[1:3])
                    elif point[3] == 'l':
                        path.lineTo(*point[1:3])
                else:
                    painter.drawArc(QRectF(*point[1:5]), *point[5:7])

            painter.drawPath(path)

        painter.end()

    def reset(self):
        self._statuses['tx'] = -1
        self._statuses['rf'] = -1
        self._statuses['rx'] = -1
        self.update()

    def resizeEvent(self, _):
        # pylint: disable=invalid-name
        self.updateSegments()

    def setStatus(self, msgs):
        # pylint: disable=invalid-name
        self._statuses['tx'] = 0
        self._statuses['rf'] = 0
        self._statuses['rx'] = 0

        if 'TX_Mute' in msgs:
            self._statuses['tx'] = 1

        if 'RF_Mute' in msgs:
            self._statuses['tx'] = -1
            self._statuses['rf'] = 1

        if 'RX_Mute' in msgs:
            self._statuses['rx'] = 1

        if 'Low_RF_Signal' in msgs:
            self._statuses['rf'] = 1

        self.update()

    def updateSegments(self):
        # pylint: disable=invalid-name
        height = self.height() - self.margin

        h_third = self.width() / 3
        diameter = min(height, h_third)
        tenth = diameter / 10
        offset = (h_third - diameter) / 2

        def _apply_offset(segment, hoffset):
            for point in segment:
                point[1] += hoffset
                point[2] += self.margin / 2

        # Determine the points to draw the following:
        #     |
        #     |
        # |‾‾‾‾|
        # |    |
        # |____|
        tx = [
            ['l', tenth * 6,         0, 'm'],
            ['l', tenth * 6, tenth * 4, 'l'],
            ['l', tenth * 8, tenth * 4, 'l'],
            ['l', tenth * 8, diameter , 'l'],
            ['l', tenth * 2, diameter , 'l'],
            ['l', tenth * 2, tenth * 4, 'l'],
            ['l', tenth * 6, tenth * 4, 'l'],
            ['l', tenth * 4, tenth * 6, 'm'],
            ['l', tenth * 6, tenth * 6, 'l'],
            ['l', tenth * 6, tenth * 7, 'l'],
            ['l', tenth * 4, tenth * 7, 'l'],
            ['l', tenth * 4, tenth * 6, 'l'],
        ]
        _apply_offset(tx, offset)

        # Determine the arcs to draw the following (but more curvaceous):
        #     ⎞
        #   ⎞ ⎟
        # ) ⎟ ⎟
        #   ⎠ ⎟
        #     ⎠
        angle_start = -60 * 16
        angle_arc = 120 * 16
        rf = [
            ['a', tenth    , tenth * 4, tenth    , tenth * 2, angle_start, angle_arc],
            ['a', tenth * 2, tenth * 3, tenth * 2, tenth * 4, angle_start, angle_arc],
            ['a', tenth * 3, tenth * 2, tenth * 3, tenth * 6, angle_start, angle_arc],
            ['a', tenth * 4, tenth    , tenth * 4, tenth * 8, angle_start, angle_arc],
        ]
        _apply_offset(rf, offset + h_third)

        # Determine the points to draw the following:
        #       |  |
        #       |  |
        # |‾‾‾‾‾‾‾‾‾‾|
        # |__________|
        rx = [
            ['l', tenth * 6, tenth * 2, 'm'],
            ['l', tenth * 6, tenth * 6, 'l'],
            ['l', diameter , tenth * 6, 'l'],
            ['l', diameter , tenth * 9, 'l'],
            ['l',         0, tenth * 9, 'l'],
            ['l',         0, tenth * 6, 'l'],
            ['l', tenth * 6, tenth * 6, 'l'],
            ['l', tenth * 9, tenth * 6, 'm'],
            ['l', tenth * 9, tenth * 2, 'l'],
            ['l', tenth * 3, tenth * 7, 'm'],
            ['l', tenth * 7, tenth * 7, 'l'],
            ['l', tenth * 7, tenth * 8, 'l'],
            ['l', tenth * 3, tenth * 8, 'l'],
            ['l', tenth * 3, tenth * 7, 'l'],
        ]
        _apply_offset(rx, offset + h_third * 2)

        self._symbols = {
            'rx': rx,
            'rf': rf,
            'tx': tx,
        }
