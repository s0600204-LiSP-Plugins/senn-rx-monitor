
from .core import MicMonitorCore
from .file_io import (
    create_blank_config,
    load_config_file,
    save_config_file,
)
from .ui.main_window import MainWindow


class Application:

    def __init__(self):
        self._monitor_core = MicMonitorCore()
        self._mainwindow = MainWindow(self)

        self.load_config()

        self._monitor_core.rx_added.connect(self.save_config)
        self._monitor_core.rx_moved.connect(self.save_config)
        self._monitor_core.rx_removed.connect(self.save_config)

    @property
    def core(self):
        return self._monitor_core

    def start(self):
        self._mainwindow.show()

    def load_config(self):
        config = load_config_file()
        for rx in config['rx']:
            self._monitor_core.append_rx(rx['ip'])

    def save_config(self, *_):
        config = create_blank_config()
        for rx in self._monitor_core.rx_list:
            config['rx'].append({
                "ip": rx,
                "proto": "mcp",
            })
        save_config_file(config)
