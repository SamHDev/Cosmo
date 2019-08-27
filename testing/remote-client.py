import remote

server = remote.TCPSocketServer(threaded=True)
client = remote.TCPSocketClient(threaded=False)


@server.client_instance
class ClientInstance(remote.TCPSocketServerInstance):
    def connect(self):
        print("Client Connected")

    def disconnect(self):
        print("Client Disconnected")

    def message(self, msg):
        print("Hello World!")
        self.send(msg)


@server.on_start
def start(host, port):
    print("Start")


@server.on_stop
def stop():
    print("Stop")


server.listen("0.0.0.0", 81)
server.start()
import time
time.sleep(1)

@client.on_open
def on_open():
    print("HELLO")
    client.send("HELLO")


@client.on_close
def on_close():
    print("CLOSE")


@client.on_message
def on_message(msg):
    print("MESSAGE")

time.sleep(1)
client.connect("localhost", 81)
