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

from lisp.core.signal import Connection, Signal
from lisp.core.util import get_lan_ip

from .timeout import Timeout

logger = logging.getLogger(__name__)

PORT = 53212
TIMEOUT_INTERVAL = 1 # seconds

class SennheiserUDPHandler(BaseRequestHandler):

    def handle(self):
        for msg in str(self.request[0].strip(), 'ascii').split('\r'):
            msg = msg.split()
            self.server.dispatch(self.client_address[0], msg[0], msg[1:])

class SennheiserUDPListener(Thread):

    def __init__(self):
        super().__init__(daemon=True)
        self.ip = get_lan_ip()
        self._server = SennheiserUDPServer((self.ip, PORT), SennheiserUDPHandler)

    def deregister(self, ip):
        return self._server.deregister(ip)

    def register(self, ip, dispatch_callback, reset_callback):
        return self._server.register(ip, dispatch_callback, reset_callback)

    def transmit(self, ip, message):
        self._server.start_timeout(ip)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(bytes(message + '\r', 'ascii'), (ip, PORT))

    def run(self):
        with self._server as server:
            logger.info("Listening for messages from Sennheiser radio-mic receivers on UDP {}:{}".format(self.ip, PORT))
            server.serve_forever()

    def stop(self):
        if self.is_alive():
            self._server.shutdown()
            self.join()


class SennheiserUDPServer(UDPServer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._registered = {}

    def deregister(self, ip):
        if ip not in self._registered:
            logger.warning("Unable to deregister device on {}, due to not being registered".format(ip))
            return False

        self._registered[ip]['dispatch'].disconnect()
        self._registered[ip]['reset_timeout'].stop()
        self._registered[ip]['reset_timeout'].end.disconnect()
        del self._registered[ip]
        return True

    def dispatch(self, source, command, attributes=[]):
        if source in self._registered:
            self._registered[source]['dispatch'].emit(command, attributes)
            self._registered[source]['reset_timeout'].restart()

    def start_timeout(self, ip):
        if ip in self._registered:
            self._registered[ip]['reset_timeout'].start()

    def register(self, ip, dispatch_callback, reset_callback):
        if ip in self._registered:
            logging.warning("Unable to register device on {}, due to a device already being registered at this address".format(ip))
            return False

        # Call the callbacks via Queued signals so as to run the callbacks on the main event thread.
        dispatch_signal = Signal()
        dispatch_signal.connect(dispatch_callback, Connection.QtQueued)

        timeout = Timeout(TIMEOUT_INTERVAL)
        timeout.end.connect(reset_callback, Connection.QtQueued)

        self._registered[ip] = {
            "dispatch": dispatch_signal,
            "reset_timeout": timeout,
        }
        return True
