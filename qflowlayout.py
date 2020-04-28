'''QFlowLayout

Code transcoded from https://doc.qt.io/qt-5/qtwidgets-layouts-flowlayout-example.html
'''

# pylint: disable=no-name-in-module
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtWidgets import QLayout, QLayoutItem, QSizePolicy, QStyle

class QFlowLayout(QLayout):
    # pylint: disable=invalid-name
    '''Implements a layout within which widget placement changes depending on the width layout'''

    def __init__(self,
                 parent=None,
                 margin: int = -1,
                 hSpacing: int = -1,
                 vSpacing: int = -1):
        super().__init__(parent)
        self._itemList = []
        self._hSpace = hSpacing
        self._vSpace = vSpacing
        self.setContentsMargins(margin, margin, margin, margin)

    def _doLayout(self,
                  rect: QRect,
                  testOnly: bool):
        # pylint: disable=too-many-locals
        '''Handles layout if horizontalSpacing or verticalSpacing don't return the default value'''
        left, top, right, bottom = self.getContentsMargins()
        effective_rect = rect.adjusted(left, top, -right, -bottom)
        x = effective_rect.x()
        y = effective_rect.y()
        line_height = 0

        for item in self._itemList:
            widget = item.widget()
            space_x = self.horizontalSpacing()
            if space_x == -1:
                space_x = widget.style().layoutSpacing(
                    QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            space_y = self.verticalSpacing()
            if space_y == -1:
                space_y = widget.style().layoutSpacing(
                    QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)

            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > effective_rect.right() and line_height > 0:
                x = effective_rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y() + bottom

    def _smartSpacing(self,
                      pm: QStyle.PixelMetric):
        '''Returns the style-specific default spacing for spacing of layouts'''
        parent = self.parent()
        if not parent:
            return -1

        if parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)

        return parent.spacing()

    def addItem(self,
                item: QLayoutItem):
        '''Add an item to the Layout'''
        self._itemList.append(item)

    def count(self):
        '''Number of items in this layout'''
        return len(self._itemList)

    def expandingDirections(self):
        # pylint: disable=no-self-use
        '''Returns the directions that this layout can make use of more space than its sizeHint()'''
        return Qt.Vertical

    def hasHeightForWidth(self):
        # pylint: disable=no-self-use
        '''The height of this layout depends on its width'''
        return True

    def heightForWidth(self,
                       width: int):
        '''Returns the height needed based on the width given'''
        return self._doLayout(QRect(0, 0, width, 0), True)

    def horizontalSpacing(self):
        '''Returns the horizontal spacing between items'''
        if self._hSpace >= 0:
            return self._hSpace
        return self._smartSpacing(QStyle.PM_LayoutHorizontalSpacing)

    def itemAt(self,
               index: int):
        '''Returns the item at the given index'''
        if -1 < index < self.count():
            return self._itemList[index]
        return None

    def minimumSize(self):
        '''Returns the minimum acceptable size of this layout'''
        size = QSize()
        for item in self._itemList:
            size = size.expandedTo(item.minimumSize())

        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size

    def setGeometry(self, rect: QRect):
        '''Calculate and layout the items'''
        super().setGeometry(rect)
        self._doLayout(rect, False)

    def sizeHint(self):
        '''Returns the size hinting for this layout'''
        return self.minimumSize()

    def takeAt(self,
               index: int):
        '''Removes and returns the item at the given index'''
        if -1 < index < self.count():
            return self._itemList.pop(index)
        return None

    def verticalSpacing(self):
        '''Returns the vertical spacing between items'''
        if self._vSpace >= 0:
            return self._vSpace
        return self._smartSpacing(QStyle.PM_LayoutHorizontalSpacing)
