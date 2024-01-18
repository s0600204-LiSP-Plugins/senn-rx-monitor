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

from qtpy.QtCore import QLineF, QSize
from qtpy.QtGui import QPainter, QPen
from qtpy.QtWidgets import QAction, QDialog, QMenu, QWidget

try:
    from lisp.ui.ui_utils import translate
except ImportError:
    from mic_rx_monitor.i18n import translate

from .add_receiver_dialog import AddReceiverDialog
from .colors import Colors
from .qflowlayout import QFlowLayout
from .rename_receiver_dialog import RenameReceiverDialog
from .widgets.drag import DRAG_MAGIC
from .widgets.mic_info import MicInfoWidget

class _DragDropIndicator:
    # pylint: disable=too-few-public-methods

    def __init__(self, parent):
        self.index = None
        self.line = None
        # The following never changes, so cache it instead of recalculating it
        # repeatedly during drag-drop operations.
        self.offset = (parent.layout().horizontalSpacing() + QPen().width()) / 2

    def reset(self):
        self.index = None
        self.line = None

class MicInfoWidgetContainer(QWidget):

    def __init__(self, monitor_core):
        super().__init__()
        self.setLayout(QFlowLayout(margin=4))
        self._size_hint = QSize(1011, 300)

        self._add_dialog = None
        self._core = monitor_core
        self._rename_dialog = None
        self._menu = QMenu(self)
        self.mouse_over_widget = None

        self.setAcceptDrops(True)
        self._drop_indicator = _DragDropIndicator(self)

        self._core.rx_added.connect(self.append_widget)
        self._core.rx_removed.connect(self.remove_widget)

        for receiver in self._core.rx_list:
            self.append_widget(receiver['addr'], self._core.rx_worker(receiver['addr']))

    def _create_menu_action(self, caption, slot, enabled=True):
        new_action = QAction(caption, parent=self._menu)
        new_action.setEnabled(enabled)
        new_action.triggered.connect(slot)
        self._menu.addAction(new_action)

    def _create_menu_subheader(self, caption):
        new_action = QAction(caption, parent=self._menu)
        new_action.setEnabled(False)
        font = new_action.font()
        font.setBold(True)
        new_action.setFont(font)
        self._menu.addAction(new_action)

    def _find_widget(self, addr):
        for item in self.layout().children():
            if item.widget().addr() == addr:
                return item.widget()
        return None

    def add_receiver(self):
        if not self._add_dialog:
            self._add_dialog = AddReceiverDialog(parent=self)

        if self._add_dialog.exec() == QDialog.Accepted:
            self._core.append_rx(self._add_dialog.addr())

    def append_widget(self, _, worker):
        widget = MicInfoWidget(worker, self._core)
        self.layout().addWidget(widget)

    def check_exists(self, addr):
        return self._core.exists(addr)

    def count(self):
        return self.layout().count()

    def contextMenuEvent(self, event):
        self._menu.clear()

        if self.mouse_over_widget and isinstance(self.mouse_over_widget, MicInfoWidget):
            self._create_menu_subheader(self.mouse_over_widget.addr())
            self._create_menu_action(
                translate('senn_rx_monitor', 'Rename Receiver'),
                self.mouse_over_widget.rename_self,
                self.mouse_over_widget.is_online
            )
            self._create_menu_action(
                translate('senn_rx_monitor', 'Remove Receiver'),
                self.mouse_over_widget.delete_self
            )
            self._menu.addSeparator()

        self._create_menu_action(
            translate('senn_rx_monitor', 'Add Receiver'),
            self.add_receiver
        )
        self._menu.popup(event.globalPos())

        self.mouse_over_widget = None

    def dragEnterEvent(self, event):
        if event.mimeData().text() == DRAG_MAGIC:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        pos = event.pos()
        child = self.childAt(pos)
        if not child:
            return

        if not isinstance(child, MicInfoWidget):
            child = child.parent()

        self._drop_indicator.index = self.layout().indexOf(child)
        rect = child.rect()
        place_before = child.mapFromParent(pos).x() < rect.width() / 2
        line = QLineF(
            child.mapToParent(rect.topLeft() if place_before else rect.topRight()),
            child.mapToParent(rect.bottomLeft() if place_before else rect.bottomRight())
        )

        if place_before:
            line.translate(-self._drop_indicator.offset, 0)
            self._drop_indicator.index -= 1
        else:
            line.translate(self._drop_indicator.offset, 0)

        self._drop_indicator.line = line
        self.update()

    def dropEvent(self, event):
        dropped = event.source().parent()
        new_index = self.layout().moveWidget(dropped, self._drop_indicator.index)
        self._drop_indicator.reset()
        self._core.move_rx(dropped.addr(), new_index)

    def minimumSize(self):
        return self.layout().minimumSize()

    def minimumSizeHint(self):
        return self._size_hint

    def paintEvent(self, _):
        if self._drop_indicator.line:
            painter = QPainter()
            painter.begin(self)
            painter.setPen(Colors.line(self))
            painter.drawLine(self._drop_indicator.line)
            painter.end()

    def remove_widget(self, addr):
        widget = self._find_widget(addr)
        self.layout().removeWidget(widget)
        widget.deleteLater()

    def request_new_receiver_name(self, old_name):
        if not self._rename_dialog:
            self._rename_dialog = RenameReceiverDialog(parent=self)

        self._rename_dialog.set_existing_name(old_name)
        if self._rename_dialog.exec() == QDialog.Accepted:
            return self._rename_dialog.name()
        return None

    def reset(self):
        item = self.layout().takeAt(0)
        while item:
            item.widget().deleteLater()
            item = self.layout().takeAt(0)
