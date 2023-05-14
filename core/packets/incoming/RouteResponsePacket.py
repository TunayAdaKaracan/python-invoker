from core.packets.Packet import *
from utils.Types import Types, Type


class RouteResponsePacket(Packet):
    def __init__(self):
        self.response_id: int = 0
        self.route_name: str = ""
        self.arg: object = None

    def getPacketID(self) -> int:
        return 0x06

    def read(self, dis: DataInputStream):
        self.response_id = dis.readInteger()
        self.route_name = dis.readString()

        argTypeStr: str = dis.readString()
        if argTypeStr != "V":
            argType: Type = Types.getTypeFromRepr(argTypeStr)
            self.arg = argType.io.read(dis)