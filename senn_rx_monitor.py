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

'''
This file is used only by the LiSP Plugin.
'''

import logging

# pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QAction

# pylint: disable=import-error
from lisp.core.has_properties import Property
from lisp.core.plugin import Plugin
from lisp.core.session import Session
from lisp.layout import register_layout
from lisp.ui.ui_utils import translate

from senn_rx_monitor.mic_rx_monitor.core import MicMonitorCore
from senn_rx_monitor.mic_rx_monitor.ui.mic_info_dialog import MicInfoDialog
from senn_rx_monitor.mic_rx_monitor.ui.mic_info_layout import MicInfoLayout

logger = logging.getLogger(__name__) # pylint: disable=invalid-name

Session.senn_rx = Property(default=[])

class SennRxMonitor(Plugin):
    """Monitoring of Sennheiser Radio Microphone Receievers"""

    Name = 'Sennheiser Rx Monitor'
    Authors = ('s0600204',)
    Description = 'Monitoring of Sennheiser Radio Microphone Receivers.'

    def __init__(self, app):
        super().__init__(app)

        self._core = MicMonitorCore()
        self._core.list_updated.connect(self.update_rx)

        MicInfoLayout.Config = SennRxMonitor.Config
        register_layout(MicInfoLayout)

        self._dialog = None
        self._menu_action = QAction(self.app.window)
        self._menu_action_discover = QAction(self.app.window)

        self.retranslateUi()

    @property
    def core(self):
        return self._core

    def _pre_session_deinitialisation(self, _):
        '''Called when session is being de-init'd.'''
        if isinstance(self.app.layout, MicInfoLayout):
            # Restore the "Edit" menu
            self.app.window.menubar.insertMenu(
                self.app.window.menuLayout.menuAction(),
                self.app.window.menuEdit
            )
            self.app.window.menuTools.removeAction(self._menu_action_discover)
        else:
            self.app.window.menuTools.removeAction(self._menu_action)

        if self._dialog:
            self._dialog.close()

        self._core.reset()

    def _on_session_initialised(self, _):
        """Post-session-initialisation init.

        Called after the plugin session-configuration have been set, but before cues have
        been restored (in the case of loading from file).
        """
        if isinstance(self.app.layout, MicInfoLayout):
            # Hide the "Edit" menu
            # This prevents the user from adding cues
            self.app.window.menubar.removeAction(
                self.app.window.menuEdit.menuAction()
            )
            self._menu_action_discover.triggered.connect(self._core.discover)
            self.app.window.menuTools.addAction(self._menu_action_discover)
        else:
            self._menu_action.triggered.connect(self._open_dialog)
            self.app.window.menuTools.addAction(self._menu_action)

        self._core.load(self.app.session.senn_rx)

    def finalize(self):
        self._core.terminate()

    def retranslateUi(self):
        self._menu_action.setIconText(
            translate('senn_rx_monitor', 'Radio Microphone Rx Status'))
        self._menu_action_discover.setIconText(
            translate('senn_rx_monitor', 'Discover RF Receivers'))

    def update_rx(self, rx_list):
        self.app.session.senn_rx = rx_list

    def _open_dialog(self):
        if not self._dialog:
            self._dialog = MicInfoDialog()
        self._dialog.open()
