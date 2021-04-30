# -*- coding: utf-8 -*-
#
# This file is a derivation of work on - and as such shares the same
# licence as - Linux Show Player
#
# Linux Show Player:
#   Copyright 2012-2020 Francesco Ceruti <ceppofrancy@gmail.com>
#
# This file:
#   Copyright 2020 s0600204
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
import socket
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

    def deregister(self, ip):
        return self._server.deregister(ip)

    def register(self, worker):
        return self._server.register(worker)

    def request_new_worker(self, ip):
        return SennheiserMCPWorker(self._server, ip)

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

    def deregister(self, ip):
        if ip not in self._registered:
            logger.warning(
                "Unable to deregister device on %s, due to not being registered",
                ip
            )
            return False

        self._clock.remove_callback(self._registered[ip].run)
        del self._registered[ip]
        return True

    def dispatch(self, source, messages):
        if source not in self._registered:
            return
        self._registered[source].receive(messages)

    def register(self, worker):
        ip = worker.ip()
        if ip in self._registered:
            logging.warning(
                "Unable to register device on %s, " \
                "due to a device already being registered at this address",
                ip
            )
            return False

        self._registered[ip] = worker
        self._clock.add_callback(worker.run)
        return True

    def transmit(self, target, message):
        if target not in self._registered:
            return
        self.socket.sendto(bytes(message + '\r', 'ascii'), (target, PORT))

class SennheiserMCPWorker:

    def __init__(self, server, ip):
        self._ip = ip
        self._server = server
        self._last_rx = None

        self.lost_connection = Signal()
        self.updated_af_level = Signal() # int, int (level, peak)
        self.updated_battery_status = Signal() # str
        self.updated_config_num = Signal() # str
        self.updated_frequency = Signal() # str
        self.updated_name = Signal() # str
        self.updated_rf = Signal() # -
        self.updated_rf_levels = Signal() # int, int (level, peak)
        self.updated_status = Signal() # array(str, ...)
        self.updated_squelch = Signal() # int

        self._handlers = {
            # Responses to specific commands
            'Name': lambda args: self.updated_name.emit(' '.join(args)),
            'Frequency': lambda args: self.updated_frequency.emit(args[0]),
            'Squelch': lambda args: self.updated_squelch.emit(int(args[0])),
            #'AfOut',
            #'Equalizer`,
            #'Mute',

            # Cyclic Attributes.
            # These are always received in the same order, and are listed in that order.
            'RF1': lambda args: self.updated_rf_levels.emit(int(args[0]), int(args[1])),
            'RF2': lambda args: self.updated_rf_levels.emit(int(args[0]), int(args[1])),
            #'States',
            'RF': lambda _: self.updated_rf.emit(),
            'AF': lambda args: self.updated_af_level.emit(int(args[0]), int(args[1])),
            'Bat': lambda args: self.updated_battery_status.emit(args[0]),
            'Msg': self.updated_status.emit,
            'Config': lambda args: self.updated_config_num.emit(args[0]),
        }

    def ip(self):
        return self._ip

    def receive(self, messages):
        '''Processes messages received from the target'''
        self._last_rx = time.monotonic()
        for msg in messages:
            msg = msg.split()
            self._handlers.get(msg[0], lambda _: None)(msg[1:])

    def request_config(self):
        self._server.transmit(self._ip, 'Push 0 0 1')

    def run(self):
        '''Code to run every UPDATE_INTERVAL'''
        self._server.transmit(self._ip, 'Push {} {} 0'.format(UPDATE_INTERVAL, UPDATE_FREQUENCY))

        if not self._last_rx or self._last_rx + UPDATE_INTERVAL > time.monotonic():
            return

        self.lost_connection.emit()
        self._last_rx = None

    def send_rename_request(self, new_name):
        self._server.transmit(self._ip, 'Name {}'.format(new_name))
