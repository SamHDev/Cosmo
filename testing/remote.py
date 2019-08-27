import socket
import threading
import time


def emptyCallback(*args, **kwargs):
    pass


class TCPSocketClient:
    def __init__(self, threaded=False, charset="UTF-8"):
        self.host = None
        self.port = None

        self.sock = socket.socket()
        self.state = 0
        self.threaded = threaded
        self.thd = None
        self.charset = charset

        self.cal_on_open = emptyCallback
        self.cal_on_close = emptyCallback
        self.cal_on_message = emptyCallback
        self.cal_on_send = emptyCallback

        self.running = True

        self.pullBuffer = None

    def connect(self, host, port):
        self.host = host
        self.port = port
        if self.host == "localhost" or self.host == "172.0.0.1":
            host = socket.gethostname()
        self.sock.connect((host, port))

        self._start()

    def main(self):
        self.cal_on_open()
        while self.running:
            recv = self.sock.recv(2048)
            if recv == b'':
                self.close()
            else:
                if self.pullBuffer:
                    self.pullBuffer = recv.decode(self.charset)
                else:
                    self.cal_on_message(recv.decode(self.charset))

    def recv(self, buffer=2048):
        self.pullBuffer = True
        while self.pullBuffer:
            pass
        buff = self.pullBuffer
        self.pullBuffer = None
        return buff

    def send(self, msg):
        self.sock.send(msg.encode(self.charset))
        self.cal_on_send(msg)

    def close(self):
        self.cal_on_close()
        self.running = False
        try:
            self.sock.close()
        except:
            pass

    def _start(self):
        if self.threaded:
            self.thd = threading.Thread(target=self.main, daemon=True)
            self.thd.start()
            time.sleep(0.1)
        else:
            self.main()
            time.sleep(0.1)

    def on_open(self, func):
        self.cal_on_open = func

    def on_message(self, func):
        self.cal_on_message = func

    def on_close(self, func):
        self.cal_on_close = func

    def on_send(self, func):
        self.cal_on_send = func


class TCPSocketServerInstance:
    def __init__(self, cr, addr, server):
        self.cr = cr
        self.addr = addr
        self.ip = self.addr[0]
        self.server = server

        self.thd = None

        self.open = False

        self.running = True

    def main(self):
        self.server.on_connect(self)
        if hasattr(self, 'connect'):
            self.connect()
        while self.server.running and self.running:
            self.recv_loop()
        self.close()

    def start(self):
        self.thd = threading.Thread(target=self.main, daemon=True)
        self.thd.start()

    def send(self, msg):
        encode = msg.encode(self.server.charset)
        self.cr.send(encode)

    def recv_loop(self):
        recv = self.cr.recv(4096)
        if recv != b'':
            decode = recv.decode(self.server.charset)
            self.server.cal_on_message(self, decode)
            if hasattr(self, 'message'):
                self.message(decode)
        else:
            self.running = False

    def recv(self):
        recv = self.cr.recv(4096)
        decode = recv.decode(self.server.charset)
        return decode

    def close(self):
        self.running = False
        try:
            self.cr.close()
        except:
            pass
        try:
            self.server.connected.remove(self)
        except:
            pass
        self.server.on_disconnect(self)
        if hasattr(self, 'disconnect'):
            self.disconnect()

    def connect(self):
        pass

    def disconnect(self):
        pass

    def message(self, msg):
        pass


class TCPSocketServer:
    def __init__(self, threaded=False, charset="UTF-8", backlog=5, instance=TCPSocketServerInstance):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.state = 0
        self.thread = None
        self.threaded = threaded
        self.charset = charset
        self.backlog = backlog
        self.thd = None
        self.instance = instance

        self.cal_on_start = emptyCallback
        self.cal_on_stop = emptyCallback
        self.cal_on_connect = emptyCallback
        self.cal_on_disconnect = emptyCallback
        self.cal_on_message = emptyCallback

        self.running = True

        self.connected = []

    def listen(self, host, port, start=False):
        self.host = host
        self.port = port
        self.sock.bind((self.host, self.port))
        if start:
            self.start()

    def main(self):
        self.cal_on_start(self.host, self.port)
        self.sock.listen(self.backlog)
        while self.running:
            cr, addr = self.sock.accept()
            inst = self.instance(cr, addr, self)
            self.connected.append(inst)
            # self.on_open(inst)
            inst.start()

    def close(self):
        self.cal_on_stop()
        self.running = False
        try:
            self.sock.close()
        except:
            pass
        self.clean_up()

    def clean_up(self):
        for c in self.connected:
            try:
                c.close()
                del c
            except:
                pass

        self.connected = []
        self.running = False

        del self.sock
        del self.thd
        del self

    def start(self):
        if self.threaded == True:
            self.thd = threading.Thread(target=self.main, daemon=True)
            self.thd.start()
            time.sleep(0.1)
        else:
            self.main()

    def on_start(self, func):
        self.cal_on_start = func

    def on_stop(self, func):
        self.cal_on_stop = func

    def on_connect(self, func):
        self.cal_on_connect = func

    def on_disconnect(self, func):
        self.cal_on_disconnect = func

    def on_message(self, func):
        self.cal_on_message = func

    def client_instance(self, class_handler):
        self.instance = class_handler
