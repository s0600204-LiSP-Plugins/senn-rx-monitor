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

import logging
from socketserver import BaseRequestHandler, UDPServer
from threading import Thread
import time

from lisp.core.clock import Clock
from lisp.core.signal import Signal

logger = logging.getLogger(__name__)

PORT = 53212

UPDATE_INTERVAL = 1 # seconds
UPDATE_FREQUENCY = 100 # milliseconds

class _Handler(BaseRequestHandler):

    def handle(self):
        # A message from an MCP device will always start with
        # an uppercase ASCII letter. Thus, ignore anything else.
        payload = self.request[0].strip()
        if 64 < payload[0] < 91:
            self.server.dispatch(
                self.client_address[0],
                str(payload, 'ascii').split('\r')
            )

class SennheiserMCPServer(Thread):

    def __init__(self):
        super().__init__(daemon=True)
        self._server = _Server(("0.0.0.0", PORT), _Handler)

    def deregister(self, addr):
        return self._server.deregister(addr)

    def register(self, worker):
        return self._server.register(worker)

    def request_new_worker(self, addr):
        return SennheiserMCPWorker(self._server, addr)

    def run(self):
        with self._server as server:
            logger.info(
                "Listening for messages from Sennheiser radio-mic receivers via UDP on port %s",
                PORT
            )
            server.serve_forever()

    def stop(self):
        if self.is_alive():
            self._server.shutdown()
            self.join()


class _Server(UDPServer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._registered = {}
        self._clock = Clock(UPDATE_INTERVAL * 1000)

    def deregister(self, addr):
        if addr not in self._registered:
            logger.warning(
                "Unable to deregister device on %s, due to not being registered",
                addr
            )
            return False

        self._clock.remove_callback(self._registered[addr].run)
        del self._registered[addr]
        return True

    def dispatch(self, source, messages):
        if source not in self._registered:
            return
        self._registered[source].receive(messages)

    def register(self, worker):
        addr = worker.addr()
        if addr in self._registered:
            logging.warning(
                "Unable to register device on %s, " \
                "due to a device already being registered at this address",
                addr
            )
            return False

        self._registered[addr] = worker
        self._clock.add_callback(worker.run)
        return True

    def transmit(self, target, message):
        if target not in self._registered:
            return
        try:
            self.socket.sendto(bytes(message + '\r', 'ascii'), (target, PORT))
        except OSError as error:
            # errno 101 == Network unreachable
            # errno 10051 == Socket operation on an unreachable network (Windows only)
            # Anything else: re-throw exception
            if error.errno not in [101, 10051]:
                raise error

class SennheiserMCPWorkerSignals:
    # pylint: disable=too-few-public-methods

    lost_connection = Signal()
    updated_af_level = Signal() # int, int (level, peak)
    updated_battery_status = Signal() # str
    updated_config_num = Signal() # str
    updated_frequency = Signal() # str
    updated_name = Signal() # str
    updated_rf = Signal() # -
    updated_rf_levels = Signal() # int, int (level, peak)
    updated_status = Signal() # array(str, ...)
    updated_squelch = Signal() # int

class SennheiserMCPWorker:

    proto = 'mcp'

    def __init__(self, server, addr):
        self._addr = addr
        self._server = server
        self._last_rx = None

        self._signals = SennheiserMCPWorkerSignals()

        self._handlers = {
            # Responses to specific commands
            'Name': lambda args: self._signals.updated_name.emit(' '.join(args)),
            'Frequency': lambda args: self._signals.updated_frequency.emit(args[0]),
            'Squelch': lambda args: self._signals.updated_squelch.emit(int(args[0])),
            #'AfOut',
            #'Equalizer`,
            #'Mute',

            # Cyclic Attributes.
            # These are always received in the same order, and are listed in that order.
            'RF1': lambda args: self._signals.updated_rf_levels.emit(int(args[0]), int(args[1])),
            'RF2': lambda args: self._signals.updated_rf_levels.emit(int(args[0]), int(args[1])),
            #'States',
            'RF': lambda _: self._signals.updated_rf.emit(),
            'AF': lambda args: self._signals.updated_af_level.emit(int(args[0]), int(args[1])),
            'Bat': lambda args: self._signals.updated_battery_status.emit(args[0]),
            'Msg': self._signals.updated_status.emit,
            'Config': lambda args: self._signals.updated_config_num.emit(args[0]),
        }

    @property
    def signals(self):
        return self._signals

    def addr(self):
        return self._addr

    def receive(self, messages):
        '''Processes messages received from the target'''
        self._last_rx = time.monotonic()
        for msg in messages:
            msg = msg.split()
            self._handlers.get(msg[0], lambda _: None)(msg[1:])

    def request_config(self):
        self._server.transmit(self._addr, 'Push 0 0 1')

    def run(self):
        '''Code to run every UPDATE_INTERVAL'''
        self._server.transmit(self._addr, 'Push {} {} 0'.format(UPDATE_INTERVAL, UPDATE_FREQUENCY))

        if not self._last_rx or self._last_rx + UPDATE_INTERVAL > time.monotonic():
            return

        self._signals.lost_connection.emit()
        self._last_rx = None

    def send_rename_request(self, new_name):
        self._server.transmit(self._addr, 'Name {}'.format(new_name))
