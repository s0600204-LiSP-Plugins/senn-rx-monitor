
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

The following receivers use a different protocol, and are not supported (at present):

* *EM 6000*
* *EM 6000 Dante*
* *EM 9046*
* *EM D1*
* *EW-DX EM 2*
* *EW-DX EM 2 Dante*
* *EW-DX EM 4 Dante*
* *SpeechLine DW*
* *SpeechLine MCR 2*
* *SpeechLine MCR 4*

The following receivers are not monitorable over an ethernet connection, but are over bluetooth:

* *EW-D EM*

Support might be possible, but requires research (and a bluetooth device).

The following receivers are not remote-monitorable, and thus will never be supported:

* Any from the *EM G2* range
* *EM 100 G3*
* *EM 100 G4*
* *EM 3731*
* *EM 3732*
* *EW-DP EK*
* *EM-XSW 1*
* *EM-XSW 1 Dual*
* *EM-XSW 2*
* *XSW-D*

And, of course, receivers from other manufacturers (e.g. *Shure*, *Trantec*) are also not supported.


Dependencies
------------

`ifaddr`_

`QDigitalMeter`_

Both these may be acquired from PyPI_ if not available from your distro's package repository.

As a Plugin
"""""""""""

*Linux Show Player*
  Specifically,  version ``0.6`` with Pull Request #144 merged.

As a Standalone Application
"""""""""""""""""""""""""""

`appdirs`_

`QDarkStyle`_

`qtpy`_

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
.. _ifaddr: https://github.com/ifaddr/ifaddr
.. _Linux Show Player: https://github.com/FrancescoCeruti/linux-show-player
.. _PyPI: https://pypi.org/
.. _QDarkStyle: https://github.com/ColinDuquesnoy/QDarkStyleSheet/
.. _QDigitalMeter: https://pypi.org/project/qdigitalmeter/
.. _qtpy: https://github.com/spyder-ide/qtpy
.. _StrictYAML: https://hitchdev.com/strictyaml/
