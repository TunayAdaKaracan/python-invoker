import threading
import socket

# TODO: Packet receiver, Getters
class Network:
    instance: "Network" = None

    def __init__(self, ip: str, port: int, authKey: str):
        if Network.instance:
            raise RuntimeError("Only one instance of Network")
        Network.instance = self
        self.ip: str = ip
        self.port: int = port
        self.authKey: str = authKey

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isRunning = False

    def start(self):
        self.__connect_until_response()

    def sendPacket(self, packet):
        pass

    def __connect_until_response(self):
        def runner():
            while not self.isRunning:
                try:
                    self.client.connect((self.ip, self.port))
                except TimeoutError:
                    self.isRunning = False
                    continue
                self.isRunning = True
        threading.Thread(target=runner, daemon=True).start()