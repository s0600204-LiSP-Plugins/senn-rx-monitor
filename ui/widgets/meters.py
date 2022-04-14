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
from PyQt5.QtGui import QLinearGradient, QColor, QPainter, QPixmap

from lisp.ui.widgets import DBMeter

class AFMeter(DBMeter):
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

    peak_map = [
        [ 5, -50],
        [10, -40],
        [15, -30],
        [25, -20],
        [45, -10],
        [95,   0],
    ]

    def __init__(self, parent=None):
        super().__init__(parent, dBMin=-50, smoothing=0, unit='dB')
        self.peak_map_keys = [v[0] for v in self.peak_map]

    def plot(self, peaks, decays):
        self.clipping = {}
        new_peaks = [self.remap_peak(peak) for peak in peaks]
        new_decays = [self.remap_peak(decay) for decay in decays]
        super().plot(new_peaks, None, new_decays)

    def remap_peak(self, peak):
        if peak in self.peak_map_keys:
            return self.peak_map[self.peak_map_keys.index(peak)][1]

        bounds = [self.peak_map_keys[0], self.peak_map_keys[-1]]
        for interval in self.peak_map_keys:
            if bounds[0] < interval < bounds[1]:
                if interval < peak:
                    bounds[0] = interval
                elif interval > peak:
                    bounds[1] = interval

        coord_a = self.peak_map[self.peak_map_keys.index(bounds[0])]
        coord_b = self.peak_map[self.peak_map_keys.index(bounds[1])]
        scale = (coord_b[1] - coord_a[1]) / (coord_b[0] - coord_a[0])
        return int(coord_a[1] + (peak - coord_a[0]) * scale)

    def reset(self):
        self.peaks = [self.dBMin]
        self.decayPeaks = [self.dBMin]
        self.clipping = {}

        self.update()

class RFMeter(DBMeter):
    # pylint: disable=attribute-defined-outside-init

    def __init__(self, parent=None):
        super().__init__(parent,
                         dBMin=0,
                         dBMax=40,
                         clipping=40,
                         unit='dBµV')
        self.scale = lambda db: db / abs(self.dBMin - self.dBMax)
        self.squelch = 1

    def plot(self, peaks, decays):
        scale = (self.dBMax - self.dBMin) / 100
        new_peaks = [self.dBMin + peak * scale for peak in peaks]
        new_decays = [self.dBMin + decay * scale for decay in decays]
        super().plot(new_peaks, None, new_decays)
        self.clipping = {}

    def setSquelch(self, squelch):
        self.squelch = squelch
        self.updatePixmap()

    def updatePixmap(self):
        """Prepare the colored rect to be used during paintEvent(s)"""
        w = self.width()
        h = self.height()

        dbRange = abs(self.dBMin - self.dBMax)
        squelch = 1 - self.squelch / dbRange

        gradient = QLinearGradient(0, 0, 0, h)
        gradient.setColorAt(0, QColor(0, 220, 0))
        gradient.setColorAt(squelch, QColor(0, 160, 0))
        gradient.setColorAt(min(squelch + 0.01, 1), QColor(255, 220, 0))
        gradient.setColorAt(1, QColor(255, 220, 0))

        self._pixmap = QPixmap(w, h)
        QPainter(self._pixmap).fillRect(0, 0, w, h, gradient)
