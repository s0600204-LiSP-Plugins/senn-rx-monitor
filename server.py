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

import socket
from socketserver import BaseRequestHandler, UDPServer
from threading import Thread

from lisp.core.util import get_lan_ip

PORT = 53212

class SennheiserUDPHandler(BaseRequestHandler):
    def handle(self):
        print(self.request)
        messages = self.request[0].strip().split('\r')
        #socket = self.request[1]
        # Do something with the data here
        # Hint: split on "\r" to get seperate messages
        for msg in messages:
            print(str(msg, 'ascii'))


class SennheiserUDPListener(Thread):

    def __init__(self):
        super().__init__(daemon=True)
        ip = get_lan_ip()
        self._server = UDPServer((ip, PORT), SennheiserUDPHandler)

    def run(self):
        with self._server as server:
            server.serve_forever()

    def stop(self):
        if self.is_alive():
            self._server.shutdown()
            self.join()


class SennheiserUDPTalker:

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, ip):
        self._ip = ip

    def send(self, msg):
        self.sock.sendto(bytes(msg + '\r', 'ascii'), (self._ip, PORT))
