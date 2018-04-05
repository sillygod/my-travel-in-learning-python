"""
"""
from collections import namedtuple
from io import BytesIO
from socket import error as socket_error

from gevent import socket
from gevent.pool import Pool
from gevent.server import StreamServer

class CommandError(Exception):
    """command error"""
    pass

class Disconnect(Exception):
    """socket disconnect"""
    pass

Error = namedtuple('Error', ('message',))

class ProtocolHandler:

    """unpack client requests and serialize server response
    """

    def handle_request(self, socket_file):
        # parse a request from the client info it's component parts.
        pass

    def write_response(self, socket_file, data):
        # serialize the response data and send it to the client.
        pass

class Server:

    def __init__(self, host='127.0.0.1', port=31337, max_client=64):
        self._pool = Pool(max_client)
        self._server = StreamServer(
            (host, port),
            self.connection_handler,
            spawn=self._pool)
        self._protocol = ProtocolHandler()
        self._kv = {}

    def connection_handler(self, conn, address):
        # Convert "conn" (a socket object) into a file-like object
        socket_file = conn.makefile('rwb')

        while True:
            try:
                data = self._protocol.handle_request(socket_file)
            except Disconnect:
                break

            try:
                resp = self.get_response(data)
            except CommandError as exec:
                resp = Error(exec.args[0])

            self._protocol.write_response(socket_file, resp)

    def get_response(self, data):
        # Here we'll actually unpack the data sent by the client, execute the 
        # command they specified, and pass back the return value.
        pass
    
    def run(self):
        self._server.serve_forever()

            

