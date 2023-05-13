from core.packets.Packet import *


class RouteRequestPacket(Packet):
    def __init__(self):
        self.route_name = None
        self.args = []

    def getPacketID(self) -> int:
        return 0x05

    def write(self, dos: "DataOutputStream"):
        super().write(dos)
        dos.writeString(self.route_name)

    # TODO
    def __parse_arguments(self):
        types = ""
        data = b""