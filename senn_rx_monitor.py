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

import logging

# pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QAction

# pylint: disable=import-error
from lisp.core.plugin import Plugin
from lisp.ui.ui_utils import translate

from .mic_info_dialog import MicInfoDialog
from .server import SennheiserUDPListener

logger = logging.getLogger(__name__) # pylint: disable=invalid-name

class SennRxMonitor(Plugin):
    """Monitoring of Sennheiser Radio Microphone Receievers"""

    Name = 'Sennheiser Rx Monitor'
    Authors = ('s0600204',)
    Description = 'Monitoring of Sennheiser Radio Microphone Receivers.'

    def __init__(self, app):
        super().__init__(app)

        self._listener = SennheiserUDPListener()
        self._listener.start()

        self._dialog = None
        self._menu_action = QAction(translate('senn_rx_monitor', 'Radio Microphone Rx Status'), self.app.window)
        self._menu_action.triggered.connect(self._open_dialog)
        self.app.window.menuTools.addAction(self._menu_action)

    def finalize(self):
        self.terminate()

    def _open_dialog(self):
        if not self._dialog:
            self._dialog = MicInfoDialog(self._listener)
        self._dialog.open()

    def terminate(self):
        self._listener.stop()
