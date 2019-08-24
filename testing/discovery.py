import socket


class DiscoveryServer:
    def __init__(self, host="", port=12892):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = False

    def listen(self):
        self.sock.bind((self.host, self.port))
        self.running = True
        self._handle()

    def _handle(self):
        while self.running:
            self.bu


