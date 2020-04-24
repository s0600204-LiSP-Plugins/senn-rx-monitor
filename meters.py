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
from PyQt5.QtGui import QLinearGradient, QColor, QPainter, QPixmap

from lisp.ui.widgets import DBMeter

class PercentageMeter(DBMeter):

    def plot(self, peaks, decay_peaks):
        # Rescale: Sennheiser gives percentages, we need dB
        scale = (self.dBMax - self.dBMin) / 100
        new_peaks = [self.dBMin + peak * scale for peak in peaks]
        new_decays = [self.dBMin + peak * scale for peak in decay_peaks]
        super().plot(new_peaks, None, new_decays)

class AFMeter(PercentageMeter):

    def __init__(self, parent=None):
        super().__init__(parent, dBMin=-50)
        self.scale = lambda db: db / abs(self.dBMin - self.dBMax) + 1

    def plot(self, *args):
        self.clipping = {}
        super().plot(*args)

    def reset(self):
        self.peaks = [self.dBMin]
        self.decayPeaks = [self.dBMin]
        self.clipping = {}

        self.update()

class RFMeter(PercentageMeter):

    def __init__(self, parent=None):
        super().__init__(parent,
                         dBMin=0,
                         dBMax=40,
                         clipping=40)
        self.scale = lambda db: db / abs(self.dBMin - self.dBMax)

    def plot(self, *args):
        super().plot(*args)
        self.clipping = {}

    def updatePixmap(self):
        """Prepare the colored rect to be used during paintEvent(s)"""
        w = self.width()
        h = self.height()

        dbRange = abs(self.dBMin - self.dBMax)

        gradient = QLinearGradient(0, 0, 0, h)
        gradient.setColorAt(0, QColor(0, 220, 0))
        gradient.setColorAt(1, QColor(0, 160, 0))

        self._pixmap = QPixmap(w, h)
        QPainter(self._pixmap).fillRect(0, 0, w, h, gradient)
