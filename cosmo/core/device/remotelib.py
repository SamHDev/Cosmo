import tcpnonblock


class RemoteServer:
    def __init__(self, host="0.0.0.0", port=12894):
        self.host = host
        self.port = port
        self.server = tcpnonblock.TCPSocketServer(threaded=True)

        self.endpoints = []


    def start(self):
        self.server.listen(self.host, self.port)
        self.start()

    def endpoint(self, name):
        print("DEC 2 ", name)
        def wrapper(func):
            self.endpoints.append(RemoteServerEndpoint(func, name))
            print("DEC 1-2 ", func)

class RemoteServerEndpoint:
    def __init__(self, func, name):
        self.func = func
        self.name = name


class RemoteServerModule:
    def __init__(self):
        pass


BashModule()