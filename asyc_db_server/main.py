"""This is a practice about simulating redis db
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

    def __init__(self):
        """according to the redis protocol, implement the corresponding handler
        """
        self.handlers = {
            b'+': self.handle_simple_string,
            b'-': self.handle_error,
            b':': self.handle_integer,
            b'$': self.handle_string,
            b'*': self.handle_array,
            b'%': self.handle_dict,
        }

    def handle_request(self, socket_file):
        # parse a request from the client info it's component parts.
        # equals to unserialize
        first_byte = socket_file.read(1)
        if not first_byte:
            raise Disconnect()

        try:
            return self.handlers[first_byte](socket_file)
        except KeyError:
            raise CommandError('bad request')
        
    def handle_simple_string(self, socket_file):
        return socket_file.readline().rstrip(b'\r\n')

    def handle_error(self, socket_file):
        return Error(socket_file.readline().rstrip(b'\r\n'))

    def handle_integer(self, socket_file):
        return int(socket_file.readline().rstrip(b'\r\n'))

    def handle_string(self, socket_file):
        length = self._parseNum(socket_file)
        if length == -1:
            return None
        
        # can not use readline.. the content may contain \r\n
        length += 2 # include the \r\n
        return socket_file.read(length)[:-2]

    def handle_array(self, socket_file):
        num = self._parseNum(socket_file)
        return [self.handle_request(socket_file) for _ in range(num)]

    def handle_dict(self, socket_file):
        num_dicts = self._parseNum(socket_file)
        elements = [self.handle_request(socket_file) for _ in range(num_dicts*2)]
        keys = elements[::2]
        values = elements[1::2]
        return dict(zip(keys, values))


    def _parseNum(self, socket_file):
        return int(socket_file.readline().rstrip(b'\r\n'))

    def write_response(self, socket_file, data):
        # serialize the response data and send it to the client.
        buf = BytesIO() 
        buf.write(self._serialize(data).encode('utf-8'))
        socket_file.write(buf.getvalue())
        socket_file.flush()
        buf.close()


    def _serialize(self, data) -> str:
        content = ''
        
        if isinstance(data, str):
            content = f"${len(data)}\r\n{data}\r\n"
        elif isinstance(data, bytes):
            content = f"${len(data)}\r\n{data.decode('utf-8')}\r\n"
        elif isinstance(data, int):
            content = f":{data}\r\n"
        elif isinstance(data, Error):
            content = f"-{data.message}\r\n"
        elif isinstance(data, (list, tuple)):
            content = f"*{len(data)}\r\n"
            return content + "".join([self._serialize(item) for item in data])
        elif isinstance(data, dict):
            content = f"%{len(data)}\r\n"
            return content + "".join([self._serialize(key)+self._serialize(value) for key, value in data.items()])
        elif data is None:
            content = "$-1\r\n"
        else:
            # cheers for python3.6 new feature: f string (performance also good)
            raise CommandError(f'unrecognized type: {type(data)}')

        return content

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
        # process the args from function do_read() for more detail
        # you can see the source in StreamServer of gevent.
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

    def get_command(self, name:str):
        if hasattr(self, name.lower()):
            func = getattr(self, name.lower())
            return func
        return None

    def get_response(self, data):
        # Here we'll actually unpack the data sent by the client, execute the 
        # command they specified, and pass back the return value.
        if not isinstance(data, list):
            try:
                data = data.split()
            except:
                raise CommandError('request must be list or string.')

        if not data:
            raise CommandError('missing command')

        command = data[0].lower().decode('utf-8')
        func = self.get_command(command)
        if func is None:
            raise CommandError(f'unrecognize command: {command}')

        return func(*data[1:])
    
    def get(self, key):
        return self._kv.get(key)

    def set(self, key, value):
        self._kv[key] = value
        return 1

    def delete(self, key):
        if key in self._kv:
            del self._kv[key]
            return 1

        return 0

    def flush(self):
        kvlen = len(self._kv)
        self._kv.clear()
        return kvlen

    def mget(self, *keys):
        return [self._kv.get(key) for key in keys]

    def mset(self, *item):
        data = zip(item[::2], item[1::2])
        for k, v in data:
            self._kv[k] = v
        return len(item) // 2

    def run(self):
        self._server.serve_forever()


class Client:

    def __init__(self, host='127.0.0.1', port='31337'):
        self._protocol = ProtocolHandler()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        self._fn = self._socket.makefile('rwb')

    def execute(self, *args):
        self._protocol.write_response(self._fn, args)
        resp = self._protocol.handle_request(self._fn)
        if isinstance(resp, Error):
            raise CommandError(resp.message)
        return resp

    def get(self, key):
        return self.execute('GET', key)
    
    def set(self, key, value):
        return self.execute('SET', key, value)

    def delete(self, key):
        return self.execute('DELETE', key)

    def flush(self):
        return self.execute('FLUSH')

    def mget(self, *keys):
        return self.execute('MGET', *keys)

    def mset(self, *items):
        return self.execute('MSET', *items)
            

if __name__ == '__main__':
    from gevent import monkey
    monkey.patch_all()

    s = Server()
    s.run()