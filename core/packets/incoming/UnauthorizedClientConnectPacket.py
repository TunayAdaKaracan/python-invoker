from core.packets.Packet import *


class UnauthorizedClientConnectPacket(Packet):
    def __init__(self):
        self.client_id: int = 0

    def getPacketID(self) -> int:
        return 0x00

    def read(self, dis: DataInputStream):
        self.client_id = dis.readInteger()