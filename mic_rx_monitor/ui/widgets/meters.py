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

from qtpy.QtGui import QLinearGradient, QColor, QPainter, QPixmap

from pyqt5_digitalmeter import DigitalMeter
from pyqt5_digitalmeter.scales import LinearScale

class AFScale(LinearScale):
    min = -50

class AFMeter(DigitalMeter):
    # pylint: disable=attribute-defined-outside-init
    '''
    AF Meter of the Sennheiser EM 300/500 G3/G4 and EM 2000 receivers.

    The values we receive from the receiver are "percentages" with
    (according to the documentation) 0% == -50 dB and 100% == "peak".
    Greater than 100% is possible. And that's all they have to say.

    Now the transition between % and dB could probably be calculated
    easily, however unfortunately my mathematical skills are limited,
    and I couldn't "see" an easy way of doing it, hence the use of an
    interpreted lookup/mapping table below.
    '''

    # [input, output, scale_factor]
    value_map = [
        [ 5, -50, 0],
        [10, -40, 0],
        [15, -30, 0],
        [25, -20, 0],
        [45, -10, 0],
        [85,   0, 0],
    ]

    # Calculate scale_factors
    _pmap = value_map[0]
    for _vmap in value_map[1:]:
        _vmap[2] = (_vmap[1] - _pmap[1]) / (_vmap[0] - _pmap[0])
        _pmap = _vmap
    del _vmap
    del _pmap

    def __init__(self, parent=None):
        super().__init__(parent,
                         scale=AFScale(),
                         smoothing=0,
                         unit='dB')

    # pylint: disable=arguments-differ
    def plot(self, peaks, decays):
        super().plot(
            [self.rescale(value) for value in peaks],
            None,
            [self.rescale(value) for value in decays])

    def rescale(self, value):
        for value_map in self.value_map:
            if value < value_map[0]:
                #        output_min + (input - input_min) * scale_factor
                return value_map[1] + (value - value_map[0]) * value_map[2]
            if value == value_map[0]:
                return value_map[1]
        return self.scale.max


from qtpy.QtCore import QPointF, QRect, QRectF, Qt, QPoint

class RFScale(LinearScale):
    max = 40
    min = 0

class RFMeter(DigitalMeter):
    # pylint: disable=attribute-defined-outside-init

    def __init__(self, parent=None):
        super().__init__(parent,
                         scale=RFScale(),
                         unit='dBµV')
        self.squelch = 1
        self._plotting_fraction = (self.scale.max - self.scale.min) / 100

    # pylint: disable=arguments-differ
    def plot(self, peaks, decays):
        super().plot(
            [self.rescale(value) for value in peaks],
            None,
            [self.rescale(value) for value in decays])

    def rescale(self, value):
        """The device returns a value between 0-100, but we need it between 0 and 40."""
        return self.scale.min + value * self._plotting_fraction

    def setSquelch(self, squelch): # pylint: disable=invalid-name
        """Valid values for squelch: 0, 5-25 (in steps of 2)"""
        self.squelch = squelch
        self.updateMeterPixmap()

    def updateMeterPixmap(self): # pylint: disable=invalid-name
        """Prepare the colored rect to be used during paintEvent(s)"""
        width = self.metersWidth()
        height = self.metersHeight()
        squelch = self.scale.scale(self.scale.max - self.squelch)

        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0, QColor(0, 220, 0))
        gradient.setColorAt(squelch, QColor(0, 160, 0))
        gradient.setColorAt(min(squelch + 0.01, 1), QColor(255, 220, 0))
        gradient.setColorAt(1, QColor(255, 220, 0))

        self._meterPixmap = QPixmap(width, height)
        QPainter(self._meterPixmap).fillRect(
            0, 0, width, height, gradient
        )
