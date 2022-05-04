
Sennheiser Rx Monitor
=====================

The **Sennheiser Rx Monitor** is a community-created plugin for `Linux Show
Player`_.

This plugin adds the ability to discover *Sennheiser*-branded radio microphones
and monitor their status across an Ethernet network from within *Linux Show
Player*.

The monitoring can be done from either a non-modal dialog (opened from the
*Tools* menu), or via the new "Radio Mic Layout" added by this plugin.


Compatibility
-------------

This plugin works with the following receivers:

* *EM 300 G3*
* *EM 500 G3*
* *EM 300-500 G4*
* *EM 2000*
* *EM 2050*

.. Note:: Firmware on these devices must be at least ``1.7.0``

This plugin will not work with the following receivers:

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

*Linux Show Player*
  Specifically, ``v0.6`` with Pull Request #144 merged.

`netifaces`_
  This can be acquired from your distro's package repository, or from PyPI_.

  And yes I'm aware that, as of May/June 2021, it's no longer maintained.


Installation
------------

To use, navigate to ``$XDG_DATA_HOME/LinuxShowPlayer/$LiSP_Version/plugins/``
(on most Linux systems ``$XDG_DATA_HOME`` is ``~/.local/share``), and create a
subfolder named ``senn_rx_monitor``.

Place the files comprising this plugin into this new folder.

When you next start **Linux Show Player**, the program should load the plugin
automatically.


.. _Linux Show Player: https://github.com/FrancescoCeruti/linux-show-player
.. _python-netifaces: https://github.com/al45tair/netifaces
.. _PyPI: https://pypi.org/project/netifaces/
