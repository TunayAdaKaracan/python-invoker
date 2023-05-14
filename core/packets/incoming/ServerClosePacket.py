from core.packets.Packet import *


class ServerClosePacket(Packet):
    def getPacketID(self) -> int:
        return 0x03