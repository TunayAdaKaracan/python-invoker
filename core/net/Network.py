import threading
import socket
from core.net.PacketSender import PacketSender
from core.net.PacketReader import PacketReader
from core.packets import Packet
from core.packets.outgoing.AuthorizationPacket import AuthorizationPacket


class Network:
    instance: "Network" = None

    def __init__(self, ip: str, port: int, authKey: str):
        if Network.instance:
            raise RuntimeError("Only one instance of Network")
        Network.instance = self
        self.ip: str = ip
        self.port: int = port
        self.authKey: str = authKey

        self.client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_id = None

        self.__isRunning: bool = False

        self.__isAuthorized = False # Make a

        self.__packet_sender: PacketSender = PacketSender(self)
        self.__packet_reader: PacketReader = PacketReader(self)


    @property
    def isRunning(self) -> bool:
        return self.__isRunning

    def start(self):
        self.__connect_until_response()
        self.__packet_sender.start()
        self.__packet_reader.start()

        auth = AuthorizationPacket()
        auth.authKey = self.authKey
        self.sendPacket(auth)

    def reconnect(self):
        self.__isRunning = False
        self.start()

    def sendPacket(self, packet: Packet):
        self.__packet_sender.addPacket(packet)

    def __connect_until_response(self):
        def runner():
            while not self.isRunning:
                try:
                    self.client.connect((self.ip, self.port))
                except TimeoutError:
                    self.__isRunning = False
                    continue
                self.__isRunning = True

        threading.Thread(target=runner, daemon=True).start()