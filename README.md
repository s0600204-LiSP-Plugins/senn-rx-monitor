
The **Sennheiser Rx Monitor** is a community-created plugin for
**[Linux Show Player](https://github.com/FrancescoCeruti/linux-show-player)**

This plugin adds the ability to monitor *Sennheiser*-branded radio microphone
receivers across an ethernet network from within **LiSP**.

This plugin works with the following receivers:

* *EM 300 G3*
* *EM 500 G3*
* *EM 300-500 G4*
* *EM 2000*
* *EM 2050*

Note: Firmware on these devices must be at least `1.7.0`

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
* Receivers from other manufacturers (e.g. *Shure*, *Trantec*)


### Installation

To use, navigate to `$XDG_DATA_HOME/LinuxShowPlayer/$LiSP_Version/plugins/` (on
most Linux systems `$XDG_DATA_HOME` is `~/.local/share`), and create a subfolder
named `senn_rx_monitor`.

Place the files comprising this plugin into this new folder.

When you next start **Linux Show Player**, the program should load the plugin
automatically.
