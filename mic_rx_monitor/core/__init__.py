
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

        self._rx_ips = [] # Used to track the display order
        self._rx_workers = {}
        self.rx_added = Signal() # ip, worker
        self.rx_moved = Signal() # ip, new_index
        self.rx_removed = Signal() # ip

    @property
    def rx_list(self):
        return tuple(self._rx_ips)

    @property
    def server(self):
        return self._server

    def add_discovered(self, ip):
        if ip in self._rx_workers:
            return
        self.append_rx(ip)

    def append_rx(self, ip):
        if ip in self._rx_workers:
            return

        if ip not in self._rx_ips:
            self._rx_ips.append(ip)

        worker = self._server.request_new_worker(ip)
        self._rx_workers[ip] = worker
        self._server.register(worker)
        self.rx_added.emit(ip, worker)

    def discover(self):
        self._discovery.discover()

    def load(self, rxs):
        for ip in rxs:
            self.append_rx(ip)

    def reset(self):
        try:
            while True:
                ip = self._rx_ips[0]
                self.remove_rx(ip)
        except IndexError:
            pass

    def move_rx(self, ip, new_index):
        self._rx_ips.remove(ip)
        self._rx_ips.insert(new_index, ip)
        self.rx_moved.emit(ip, new_index)

    def remove_rx(self, ip):
        if ip not in self._rx_workers:
            return

        self._server.deregister(ip)
        self._rx_ips.remove(ip)
        self.rx_removed.emit(ip)
        del self._rx_workers[ip]

    def rx_worker(self, ip):
        if ip in self._rx_workers:
            return self._rx_workers[ip]
        return None

    def terminate(self):
        self._server.stop()
