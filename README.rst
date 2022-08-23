
Sennheiser Rx Monitor
=====================

The **Sennheiser Rx Monitor** is a community-created utility that may be used
as a plugin for `Linux Show Player`_ or as a standalone application.

This utility has the ability to discover *Sennheiser*-branded radio microphones,
and monitor their status across an Ethernet network.

When used as a plugin, the monitoring can be done from either a non-modal dialog
(opened from the *Tools* menu), or via the "Radio Mic Layout" that is also
provided.


Compatibility
-------------

The following receivers are supported:

* *EM 300 G3*
* *EM 500 G3*
* *EM 300-500 G4*
* *EM 2000*
* *EM 2050*

.. Note:: Firmware on these devices must be at least ``1.7.0``

The following receivers are not:

* Any from the *EM G2* range
* *EM 100 G3*
* *EM 100 G4*
* *EM 3731*
* *EM 3732*
* *EM 6000*
* *EM 6000 Dante*
* *EM 9046*
* *EM D1*
* *EW-D EM*
* Receivers from other manufacturers (e.g. *Shure*, *Trantec*)


Dependencies
------------

`netifaces`_
  A python module that can be acquired from your distro's package repository, or from PyPI_.

  And yes I'm aware that, as of May/June 2021, it's no longer maintained.

As a Plugin
"""""""""""

*Linux Show Player*
  Specifically,  version ``0.6`` with Pull Request #144 merged.

As a Standalone Application
"""""""""""""""""""""""""""

`appdirs`_

`PyQt5`_

`QDarkStyle`_

`StrictYAML`_

All of these are installed automatically by ``pip`` if not already installed.


Installation
------------

To install as a Plugin
""""""""""""""""""""""

Navigate to ``$XDG_DATA_HOME/LinuxShowPlayer/$LiSP_Version/plugins/``
(on most Linux systems ``$XDG_DATA_HOME`` is ``~/.local/share``), and create a
subfolder named ``senn_rx_monitor``.

Place the files comprising this project into this new folder.

When you next start **Linux Show Player**, the program should load the plugin
automatically.

To install as a Standalone Application
""""""""""""""""""""""""""""""""""""""

Clone the repository locally, and run ``pip install .`` (with elevated
privileges if necessary) from its root folder.

To run: call ``senn-rx-monitor`` from the command line.


.. _appdirs: https://github.com/ActiveState/appdirs
.. _Linux Show Player: https://github.com/FrancescoCeruti/linux-show-player
.. _netifaces: https://github.com/al45tair/netifaces
.. _PyPI: https://pypi.org/
.. _PyQt5: https://www.riverbankcomputing.com/software/pyqt/
.. _QDarkStyle: https://github.com/ColinDuquesnoy/QDarkStyleSheet/
.. _StrictYAML: https://hitchdev.com/strictyaml/
