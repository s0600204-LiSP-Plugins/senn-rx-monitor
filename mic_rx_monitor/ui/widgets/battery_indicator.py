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

import copy

from qtpy.QtCore import Qt, QRect
from qtpy.QtGui import QPainter, QPainterPath
from qtpy.QtWidgets import QWidget

try:
    from lisp.ui.ui_utils import translate
except ImportError:
    from mic_rx_monitor.i18n import translate

from ..colors import Colors


class BatteryIndicator(QWidget):

    margin = 6

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.setMinimumHeight(28)
        self._segments = []
        self._filled = -1
        self._segment_count = 3

        self._no_battery_msg = ''
        self.retranslateUi()

    def retranslateUi(self):
        self._no_battery_msg = translate('senn_rx_monitor', "No Batt. Status")

    def paintEvent(self, _):
        # pylint: disable=invalid-name
        height = self.height()
        width = self.width()

        painter = QPainter()
        painter.begin(self)

        painter.setBrush(Colors.background(self))
        painter.setPen(Colors.line(self))
        painter.drawRect(QRect(0, 0, width - 1, height - 1))

        if self._filled == -1:
            painter.drawText(0, 0, width, height, Qt.AlignCenter, self._no_battery_msg)
            painter.end()
            return

        painter.setRenderHint(QPainter.Antialiasing, True)
        if self._filled == 0:
            painter.setPen(Colors.error(self))
        else:
            painter.setPen(Colors.ok(self))

        for seg_num, segment in enumerate(self._segments):
            path = QPainterPath()
            for p_num, point in enumerate(segment):
                if p_num == 0:
                    path.moveTo(*point)
                else:
                    path.lineTo(*point)
            path.closeSubpath()
            if seg_num < self._filled:
                painter.setBrush(Colors.ok(self))
            else:
                painter.setBrush(Colors.background(self))

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
        jut = height / 5
        vgrid = (width - self.margin * (self._segment_count - 1)) / (self._segment_count * 3 - 2)
        offset = self.margin

        def _apply_offset(segment, hoffset):
            for point in segment:
                point[0] += hoffset
                point[1] += self.margin

        # |‾‾/
        # |_/
        left_segment = [
            [0, 0],
            [vgrid * 2 + jut, 0],
            [vgrid * 2 - jut, height],
            [0, height]
        ]
        _apply_offset(left_segment, offset)
        self._segments.append(left_segment)
        offset += vgrid * 2 + self.margin

        #  /‾‾/
        # /__/
        centre_segment = [
            [jut, 0],
            [vgrid * 3 + jut, 0],
            [vgrid * 3 - jut, height],
            [-jut, height]
        ]
        for _ in range(self._segment_count - 2):
            cs = copy.deepcopy(centre_segment)
            _apply_offset(cs, offset)
            self._segments.append(cs)
            offset += vgrid * 3 + self.margin

        #  /‾|
        # /__|
        right_segment = [
            [jut, 0],
            [vgrid * 2, 0],
            [vgrid * 2, height],
            [-jut, height]
        ]
        _apply_offset(right_segment, offset)
        self._segments.append(right_segment)
