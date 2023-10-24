import abc
import uuid
from typing import Union

from datastream import DataOutputStream, DataInputStream
from typeio import Types, Type


class Packet(abc.ABC):
    @abc.abstractmethod
    def getPacketID(self) -> int:
        pass

    def write(self, dos: DataOutputStream):
        dos.writeInteger(self.getPacketID())

    def read(self, dis: DataInputStream):
        pass

    def send(self, network):
        network.sendPacket(self)


class ClientConnectPacket(Packet):
    def __init__(self):
        self.client_id = 0

    def getPacketID(self) -> int:
        return 0x01

    def read(self, dis: DataInputStream):
        self.client_id = uuid.UUID(dis.readString())


class ClientDisconnectPacket(Packet):
    def __init__(self):
        self.client_id = 0

    def getPacketID(self) -> int:
        return 0x02

    def read(self, dis: DataInputStream):
        self.client_id = uuid.UUID(dis.readString())


class InformationPacket(Packet):
    def __init__(self):
        self.client_id = 0

    def getPacketID(self) -> int:
        return 0x08

    def read(self, dis: DataInputStream):
        self.client_id = uuid.UUID(dis.readString())


class RouteNotFoundPacket(Packet):
    def __init__(self):
        self.route_id = 0
        self.route_name: str = ""

    def getPacketID(self) -> int:
        return 0x07

    def read(self, dis: DataInputStream):
        self.route_id = uuid.UUID(dis.readString())
        self.route_name = dis.readString()


class RouteInvokeErrorPacket(Packet):
    def __init__(self):
        self.route_id = 0
        self.route_name = ""
        self.error_message = ""

    def getPacketID(self) -> int:
        return 0x0B

    def read(self, dis: DataInputStream):
        self.route_id = uuid.UUID(dis.readString())
        self.route_name = dis.readString()
        self.error_message = dis.readString()


class RouteResponsePacket(Packet):
    def __init__(self):
        self.response_id = 0
        self.route_name: str = ""
        self.arg: object = None

    def getPacketID(self) -> int:
        return 0x06

    def read(self, dis: DataInputStream):
        self.response_id = uuid.UUID(dis.readString())
        self.route_name = dis.readString()

        argTypeStr: str = dis.readString()
        if argTypeStr != "V":
            argType: Type = Types.getTypeFromRepr(argTypeStr)
            self.arg = argType.io.read(dis)


class ServerClosePacket(Packet):
    def getPacketID(self) -> int:
        return 0x03


class AuthorizationPacket(Packet):
    def __init__(self):
        self.authKey = None

    def getPacketID(self) -> int:
        return 0x04

    def write(self, dos: DataOutputStream):
        super().write(dos)
        dos.writeString(self.authKey)


class RouteRequestPacket(Packet):
    def __init__(self):
        self.uuid = None
        self.route_name = None
        self.args = []

    def getPacketID(self) -> int:
        return 0x05

    def write(self, dos: DataOutputStream):
        super().write(dos)
        dos.writeString(str(self.uuid))
        dos.writeString(self.route_name)
        self.__parse_arguments(dos)

    def __parse_arguments(self, dos: DataOutputStream):
        types = ""
        sendData = []
        for arg in self.args:
            argType = Types.getTypeFromArg(arg)
            assert argType is not None  # TODO: Error handling
            types += argType.repr
            sendData.append((arg, argType))
        dos.writeString(types)
        for element in sendData:
            argType: Type = element[1]
            argType.io.write(dos, element[0])


class ServerRejectedClientPacket(Packet):
    def getPacketID(self) -> int:
        return 0x09


class EnableCustomPacketPacket(Packet):
    def __init__(self):
        self.packet_id = 0

    def getPacketID(self) -> int:
        return 0x0A

    def write(self, dos: DataOutputStream):
        super().write(dos)
        dos.writeInteger(self.packet_id)


class PacketFactory:
    packets: [int, object] = {}

    @staticmethod
    def registerPacket(packetID: int, supplier):
        PacketFactory.packets[packetID] = supplier

    @staticmethod
    def getPacketFromID(ID: int) -> Union[None, Packet]:
        if ID not in PacketFactory.packets:
            return None
        return PacketFactory.packets[ID]()


PacketFactory.registerPacket(ClientConnectPacket().getPacketID(), ClientConnectPacket)
PacketFactory.registerPacket(ClientDisconnectPacket().getPacketID(), ClientDisconnectPacket)
PacketFactory.registerPacket(InformationPacket().getPacketID(), InformationPacket)
PacketFactory.registerPacket(RouteNotFoundPacket().getPacketID(), RouteNotFoundPacket)
PacketFactory.registerPacket(RouteResponsePacket().getPacketID(), RouteResponsePacket)
PacketFactory.registerPacket(ServerClosePacket().getPacketID(), ServerClosePacket)
PacketFactory.registerPacket(ServerRejectedClientPacket().getPacketID(), ServerRejectedClientPacket)
