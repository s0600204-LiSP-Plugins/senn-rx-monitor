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

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLabel, QLineEdit

try:
    from lisp.ui.ui_utils import translate
except ImportError:
    from mic_rx_monitor.i18n import translate

class RenameReceiverDialog(QDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setWindowModality(Qt.WindowModal)
        self.setLayout(QFormLayout())

        self._label = QLabel()
        self._label.setAlignment(Qt.AlignHCenter)
        self.layout().addRow(self._label)

        self._name_text = QLineEdit()
        self._name_text.setMaxLength(8)
        self.layout().addRow('-', self._name_text)

        self._buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Close)
        self._buttons.accepted.connect(self.validate)
        self._buttons.rejected.connect(self.reject)
        self.layout().addRow(self._buttons)

    def name(self):
        return self._name_text.text()

    def exec(self):
        self.retranslateUi()
        return super().exec()

    def retranslateUi(self):
        self.setWindowTitle(
            translate('senn_rx_monitor', 'Rename Receiver'))
        self._label.setText(
            translate('senn_rx_monitor', 'Enter a new name'))
        self.layout().labelForField(self._name_text).setText(
            translate('senn_rx_monitor', 'New Name:'))

    def set_existing_name(self, existing_name):
        self._name_text.setPlaceholderText(existing_name)
        self._name_text.setText(existing_name)

    def validate(self):
        try:
            bytes(self._name_text.text(), 'ascii', 'strict')
        except UnicodeEncodeError:
            self._label.setText(translate('senn_rx_monitor', 'Not a valid name'))
            return
        self.accept()
