from core.packets.Packet import *


class RouteNotFoundPacket(Packet):
    def __init__(self):
        self.route_name: str = ""

    def getPacketID(self) -> int:
        return 0x07

    def read(self, dis: DataInputStream):
        self.route_name = dis.readString()