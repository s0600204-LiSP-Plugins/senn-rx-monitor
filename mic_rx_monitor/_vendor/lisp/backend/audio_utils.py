# This file is part of Linux Show Player
#
# Copyright 2022 Francesco Ceruti <ceppofrancy@gmail.com>
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


def iec_scale(dB):
    """IEC 268-18:1995 standard dB scaling.

    adapted from: http://plugin.org.uk/meterbridge/
    """
    scale = 100

    if dB < -70.0:
        scale = 0.0
    elif dB < -60.0:
        scale = (dB + 70.0) * 0.25
    elif dB < -50.0:
        scale = (dB + 60.0) * 0.50 + 5
    elif dB < -40.0:
        scale = (dB + 50.0) * 0.75 + 7.5
    elif dB < -30.0:
        scale = (dB + 40.0) * 1.5 + 15
    elif dB < -20.0:
        scale = (dB + 30.0) * 2.0 + 30
    elif dB < 0:
        scale = (dB + 20.0) * 2.5 + 50

    return scale / 100
