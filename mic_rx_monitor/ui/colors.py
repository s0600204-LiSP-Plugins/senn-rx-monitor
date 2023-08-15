
import enum

from PyQt5.QtGui import QColor

"""
If a Theme does not explicitly set palette colours, Qt5 derives suitable colours from the
Theme's stylesheet.

From experimentation it appears that, for any given widget, the colours given to the derived
Palette's `ColorRole`s are taken from the following QSS properties:

  Palette `ColorRole`  QSS Property
  -------------------  --------------------------
  Window               background-color
  WindowText           color
  Base                 background-color
  AlternateBase        alternate-background-color
  ToolTipBase          -
  ToolTipText          -
  PlaceholderText      color
  Text                 color
  Button               background-color
  ButtonText           color
  BrightText           -
  Light                -
  Midlight             -
  Dark                 -
  Mid                  -
  Shadow               -
  Highlight            selection-background-color
  HighlightedText      selection-color
  Link                 -
  LinkVisited          -

If the applicable property is not set in the stylesheet, or the ColorRole is not derived from
any QSS property, then the colour for that ColorRole remains at the system default.

It is worth pointing out that the `border-color` QSS property is not mapped anywhere, making
the use of it to define the colour of lines or custom borders in custom widgets very difficult,
if not impossible.

It is also worth pointing out that this derivation of colours and setting them on a widget's
palette only seems to occur as part of the painting process - requesting a widget's palette
outside of a `paintEvent()` call (or the "Application Palette" at any time) results in a palette
populated only with the default system colours.

@see https://github.com/qt/qtbase/blob/dev/src/gui/text/qcssparser.cpp
     ValueExtractor::extractPalette [~L1343]
     @note: Extracts `Color`, `SelectionForeground`, `SelectionBackground`, `AlternateBackground`

@see https://github.com/qt/qtbase/blob/dev/src/widgets/styles/qstylesheetstyle.cpp
     configurePalette() ~L1452
     @note: [~L508]
        `bg` == "Background Data" incl. `background-color`
        `pal` == "Palette Data" (extracted by ValueExtractor::extractPalette)

"""

class Colors:

    class State(enum.Enum):
        NORMAL = enum.auto()
        HOVER = enum.auto()

    OK = QColor(0, 160, 0)
    ERROR = QColor(250, 0, 0)

    @classmethod
    def ok(cls, _):
        return cls.OK

    @classmethod
    def error(cls, _):
        return cls.ERROR

    @classmethod
    def line(cls, widget_instance, state=State.NORMAL):
        if state == cls.State.HOVER:
            return widget_instance.palette().text().color()
        return widget_instance.palette().shadow().color()

    @classmethod
    def background(cls, widget_instance):
        return widget_instance.palette().window().color().darker(113)

    @classmethod
    def fill(cls, widget_instance):
        return widget_instance.palette().window().color().darker(175)
