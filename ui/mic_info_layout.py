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

from lisp.layout.cue_layout import CueLayout
from lisp.plugins import get_plugin
from lisp.ui.ui_utils import translate

from .mic_info_widget_container import MicInfoWidgetContainer

class MicInfoLayout(CueLayout):
    NAME = translate("LayoutName", "Radio Mic Layout")
    DESCRIPTION = translate(
        "LayoutDescription", "Monitor Radio Microphones"
    )
    DETAILS = [
        translate("LayoutDetails", "Useful for monitoring stations"),
    ]

    def __init__(self, application):
        super().__init__(application)

        listener = get_plugin('SennRxMonitor').listener()
        self._container = MicInfoWidgetContainer(listener)

        self.app.session_initialised.connect(self.load)

    def load(self):
        for ip in self.app.session.senn_rx:
            self._container.append_widget(ip)

    def cue_at(self, *_):
        raise IndexError("Layout does not support cues")

    def cues(self, *_):
        return []

    def deselect_all(self, *_):
        pass

    def finalize(self):
        self._container.reset()
        self.app.session_initialised.disconnect(self.load)

    def invert_selection(self):
        pass

    @property
    def model(self):
        return None

    def select_all(self, *_):
        pass

    def selected_cues(self, *_):
        return []

    @property
    def view(self):
        return self._container
