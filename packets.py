import abc
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
        self.client_id: int = 0

    def getPacketID(self) -> int:
        return 0x01

    def read(self, dis: DataInputStream):
        self.client_id = dis.readInteger()


class ClientDisconnectPacket(Packet):
    def __init__(self):
        self.client_id: int = 0

    def getPacketID(self) -> int:
        return 0x02

    def read(self, dis: DataInputStream):
        self.client_id = dis.readInteger()


class InformationPacket(Packet):
    def __init__(self):
        self.client_id: int = 0

    def getPacketID(self) -> int:
        return 0x08

    def read(self, dis: DataInputStream):
        self.client_id = dis.readInteger()


class RouteNotFoundPacket(Packet):
    def __init__(self):
        self.route_name: str = ""
        self.route_id: int = 0

    def getPacketID(self) -> int:
        return 0x07

    def read(self, dis: DataInputStream):
        self.route_id = dis.readInteger()
        self.route_name = dis.readString()


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


class ServerClosePacket(Packet):
    def getPacketID(self) -> int:
        return 0x03


class UnauthorizedClientConnectPacket(Packet):
    def __init__(self):
        self.client_id: int = 0

    def getPacketID(self) -> int:
        return 0x00

    def read(self, dis: DataInputStream):
        self.client_id = dis.readInteger()


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
        self.route_name = None
        self.args = []

    def getPacketID(self) -> int:
        return 0x05

    def write(self, dos: DataOutputStream):
        super().write(dos)
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


# TODO: Register Incoming Packets
PacketFactory.registerPacket(ClientConnectPacket().getPacketID(), ClientConnectPacket)
PacketFactory.registerPacket(ClientDisconnectPacket().getPacketID(), ClientDisconnectPacket)
PacketFactory.registerPacket(InformationPacket().getPacketID(), InformationPacket)
PacketFactory.registerPacket(RouteNotFoundPacket().getPacketID(), RouteNotFoundPacket)
PacketFactory.registerPacket(RouteResponsePacket().getPacketID(), RouteResponsePacket)
PacketFactory.registerPacket(ServerClosePacket().getPacketID(), ServerClosePacket)
PacketFactory.registerPacket(UnauthorizedClientConnectPacket().getPacketID(), UnauthorizedClientConnectPacket)
PacketFactory.registerPacket(ServerRejectedClientPacket().getPacketID(), ServerRejectedClientPacket)


class EventRegistry:
    events: [int, [callable]] = {}

    @staticmethod
    def _register(packet_id: int, event: callable):
        if packet_id not in EventRegistry.events:
            EventRegistry.events[packet_id] = []

        EventRegistry.events[packet_id].append(event)

    @staticmethod
    def fireEvent(network, packet_id: int, packet: Packet):
        if packet_id in EventRegistry.events:
            for event in EventRegistry.events[packet_id]:
                event(network, packet)

    @staticmethod
    def findIDFromClass(cls):
        for id, clazz in PacketFactory.packets.items():
            if cls == clazz:
                return id
        return None


def packet_event(packet_class):
    def decorator(func):
        if EventRegistry.findIDFromClass(packet_class) is None:
            raise RuntimeError("There is no such a packet")

        EventRegistry._register(EventRegistry.findIDFromClass(packet_class), func)

        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return decorator