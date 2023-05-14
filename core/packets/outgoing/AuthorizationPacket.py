from core.packets.Packet import *


class AuthorizationPacket(Packet):
    def __init__(self):
        self.authKey = None

    def getPacketID(self) -> int:
        return 0x04

    def write(self, dos: DataOutputStream):
        super().write(dos)
        dos.writeString(self.authKey)