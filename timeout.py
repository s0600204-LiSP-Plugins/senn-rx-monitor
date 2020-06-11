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

from threading import Timer

from lisp.core.signal import Signal

class Timeout:

    def __init__(self, interval):
        self._interval = interval
        self.end = Signal()
        self.timer = None

    def fire(self):
        self.end.emit()

    def start(self):
        if self.timer:
            return
        self.timer = Timer(self._interval, self.fire)
        self.timer.start()

    def stop(self):
        if not self.timer:
            return
        if self.timer.is_alive():
            self.timer.cancel()
        self.timer = None

    def restart(self):
        self.stop()
        self.start()
