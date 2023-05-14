from core.packets.Packet import *
from utils.Types import Types, Type


class RouteRequestPacket(Packet):
    def __init__(self):
        self.route_name = None
        self.args = []

    def getPacketID(self) -> int:
        return 0x05

    def write(self, dos: DataOutputStream):
        super().write(dos)
        dos.writeString(self.route_name)
        self.__parse_arguments(dos)

    # TODO
    def __parse_arguments(self, dos: DataOutputStream):
        types = ""
        sendData = []
        for arg in self.args:
            argType = Types.getTypeFromArg(arg)
            assert argType is not None #TODO: Error handling
            types += argType.repr
            sendData.append((arg, argType))
        for element in sendData:
            argType: Type = element[1]
            argType.io.write(dos, element[0])