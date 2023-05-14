from core.packets.Packet import *


class ClientConnectPacket(Packet):
    def __init__(self):
        self.client_id: int = 0

    def getPacketID(self) -> int:
        return 0x01

    def read(self, dis: DataInputStream):
        self.client_id = dis.readInteger()