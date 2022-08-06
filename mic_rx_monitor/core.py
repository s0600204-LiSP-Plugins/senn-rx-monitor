
from lisp.core.signal import Connection, Signal

try:
    # When accessed as a plugin
    from senn_rx_monitor.mic_rx_monitor.discovery.mcp_discovery import SennheiserMCPDiscovery
    from senn_rx_monitor.mic_rx_monitor.servers.mcp_server import SennheiserMCPServer
except ImportError:
    # And as a stand-alone program
    from mic_rx_monitor.discovery.mcp_discovery import SennheiserMCPDiscovery
    from mic_rx_monitor.servers.mcp_server import SennheiserMCPServer


class MicMonitorCore:

    def __init__(self):

        self._server = SennheiserMCPServer()
        self._server.start()

        self._discovery = SennheiserMCPDiscovery()
        self._discovery.start()
        self._discovery.discovered.connect(self.add_discovered, Connection.QtQueued)

        self._rx_addrs = [] # Used to track the display order
        self._rx_workers = {}
        self.rx_added = Signal() # addr, worker
        self.rx_moved = Signal() # addr, new_index
        self.rx_removed = Signal() # addr
        self.list_updated = Signal() # rx_list

    @property
    def rx_list(self):
        lst = []
        for addr in self._rx_addrs:
            lst.append({
                "addr": addr,
                "proto": self._rx_workers[addr].proto,
            })
        return lst

    @property
    def server(self):
        return self._server

    def add_discovered(self, addr):
        if addr in self._rx_workers:
            return
        self.append_rx(addr)

    def append_rx(self, addr):
        if addr in self._rx_workers:
            return

        if addr not in self._rx_addrs:
            self._rx_addrs.append(addr)

        worker = self._server.request_new_worker(addr)
        self._rx_workers[addr] = worker
        self._server.register(worker)
        self.rx_added.emit(addr, worker)
        self.list_updated.emit(self.rx_list)

    def discover(self):
        self._discovery.discover()

    def exists(self, addr):
        return addr in self._rx_workers

    def load(self, rx_list):
        for receiver in rx_list:
            if isinstance(receiver, str):
                # Backwards compatibility with old LiSP showfiles
                self.append_rx(receiver)
            else:
                self.append_rx(receiver['addr'])

    def reset(self):
        try:
            while True:
                addr = self._rx_addrs[0]
                self.remove_rx(addr)
        except IndexError:
            pass

    def move_rx(self, addr, new_index):
        self._rx_addrs.remove(addr)
        self._rx_addrs.insert(new_index, addr)
        self.rx_moved.emit(addr, new_index)
        self.list_updated.emit(self.rx_list)

    def remove_rx(self, addr):
        if addr not in self._rx_workers:
            return

        self._server.deregister(addr)
        self._rx_addrs.remove(addr)
        self.rx_removed.emit(addr)
        self.list_updated.emit(self.rx_list)
        del self._rx_workers[addr]

    def rx_worker(self, addr):
        if addr in self._rx_workers:
            return self._rx_workers[addr]
        return None

    def terminate(self):
        self._server.stop()
