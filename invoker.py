import abc
import socket
import struct
import threading
from queue import Queue
from typing import Union


class Printer:
    instance: Union[None, "Printer"] = None

    def __init__(self):
        Printer.instance = self
        self.toPrint = []
        threading.Thread(target=self.print_while, daemon=True).start()

    @staticmethod
    def print(line):
        Printer.instance.toPrint.append(line)

    def print_while(self):
        while True:
            if len(self.toPrint) != 0:
                print(self.toPrint.pop(0))


Printer()


def readNByte(sock: socket.socket, n: int) -> bytes:
    data = b""
    while not data:
        data = sock.recv(n)
    return data


def readByte(sock: socket.socket) -> int:
    return struct.unpack(">b", readNByte(sock, 1))[0]


def readShort(sock: socket.socket) -> int:
    return struct.unpack(">h", readNByte(sock, 1))[0]


def readInteger(sock: socket.socket) -> int:
    return struct.unpack(">i", readNByte(sock, 4))[0]


def readDouble(sock: socket.socket) -> float:
    return struct.unpack(">d", readNByte(sock, 8))[0]


def readFloat(sock: socket.socket) -> float:
    return struct.unpack(">f", readNByte(sock, 4))[0]


def readLong(sock: socket.socket) -> int:
    return struct.unpack(">l", readNByte(sock, 4))[0]


def readUnsignedByte(sock: socket.socket) -> int:
    return struct.unpack(">B", readNByte(sock, 1))[0]


def readUnsignedShort(sock: socket.socket) -> int:
    return struct.unpack(">H", readNByte(sock, 2))[0]


def readUnsignedInteger(sock: socket.socket) -> int:
    return struct.unpack(">I", readNByte(sock, 4))[0]


def readUnsignedDouble(sock: socket.socket) -> float:
    return struct.unpack(">D", readNByte(sock, 8))[0]


def readUnsignedFloat(sock: socket.socket) -> float:
    return struct.unpack(">F", readNByte(sock, 4))[0]


def readUnsignedLong(sock: socket.socket) -> int:
    return struct.unpack(">L", readNByte(sock, 4))[0]


def readString(sock: socket.socket) -> str:
    strlen = readUnsignedShort(sock)
    return readNByte(sock, strlen).decode("utf-8")


def writeBytes(sock: socket.socket, b: bytes):
    sock.send(b)


def writeByte(sock: socket.socket, v: int):
    writeBytes(sock, struct.pack(">b", v))


def writeShort(sock: socket.socket, v: int):
    writeBytes(sock, struct.pack(">h", v))


def writeInteger(sock: socket.socket, v: int):
    writeBytes(sock, struct.pack(">i", v))


def writeDouble(sock: socket.socket, v: float):
    writeBytes(sock, struct.pack(">d", v))


def writeFloat(sock: socket.socket, v: float):
    writeBytes(sock, struct.pack(">f", v))


def writeLong(sock: socket.socket, v: int):
    writeBytes(sock, struct.pack(">l", v))


def writeUnsignedByte(sock: socket.socket, v: int):
    writeBytes(sock, struct.pack(">B", v))


def writeUnsignedShort(sock: socket.socket, v: int):
    writeBytes(sock, struct.pack(">H", v))


def writeUnsignedInteger(sock: socket.socket, v: int):
    writeBytes(sock, struct.pack(">I", v))


def writeUnsignedDouble(sock: socket.socket, v: float):
    writeBytes(sock, struct.pack(">D", v))


def writeUnsignedFloat(sock: socket.socket, v: float):
    writeBytes(sock, struct.pack(">F", v))


def writeUnsignedLong(sock: socket.socket, v: int):
    writeBytes(sock, struct.pack(">L", v))


def writeString(sock: socket.socket, v: str):
    writeBytes(sock, struct.pack(">H", len(v)) + v.encode("utf-8"))


class DataStream:
    def __init__(self, sock: socket.socket):
        self.sock = sock

    def getSocket(self) -> socket.socket:
        return self.sock


class DataOutputStream(DataStream):
    def __init__(self, sock: socket.socket):
        super().__init__(sock)

    def writeBytes(self, b: bytes):
        writeBytes(self.sock, b)

    def writeByte(self, v: int):
        writeByte(self.sock, v)

    def writeShort(self, v: int):
        writeShort(self.sock, v)

    def writeInteger(self, v: int):
        writeInteger(self.sock, v)

    def writeDouble(self, v: float):
        writeDouble(self.sock, v)

    def writeFloat(self, v: float):
        writeFloat(self.sock, v)

    def writeLong(self, v: int):
        writeLong(self.sock, v)

    def writeUnsignedByte(self, v: int):
        writeUnsignedByte(self.sock, v)

    def writeUnsignedShort(self, v: int):
        writeUnsignedShort(self.sock, v)

    def writeUnsignedInteger(self, v: int):
        writeUnsignedInteger(self.sock, v)

    def writeUnsignedDouble(self, v: float):
        writeUnsignedDouble(self.sock, v)

    def writeUnsignedFloat(self, v: float):
        writeUnsignedFloat(self.sock, v)

    def writeUnsignedLong(self, v: int):
        writeUnsignedLong(self.sock, v)

    def writeString(self, v: str):
        writeString(self.sock, v)


class DataInputStream(DataStream):
    def __init__(self, sock: socket.socket):
        super().__init__(sock)

    def readNByte(self, n: int) -> bytes:
        return readNByte(self.sock, n)

    def readByte(self) -> int:
        return readByte(self.sock)

    def readShort(self) -> int:
        return readShort(self.sock)

    def readInteger(self) -> int:
        return readInteger(self.sock)

    def readLong(self) -> int:
        return readLong(self.sock)

    def readDouble(self) -> float:
        return readDouble(self.sock)

    def readFloat(self) -> float:
        return readFloat(self.sock)

    def readUnsignedByte(self) -> int:
        return readUnsignedByte(self.sock)

    def readUnsignedShort(self) -> int:
        return readUnsignedShort(self.sock)

    def readUnsignedInteger(self) -> int:
        return readUnsignedInteger(self.sock)

    def readUnsignedLong(self) -> int:
        return readUnsignedLong(self.sock)

    def readUnsignedDouble(self) -> float:
        return readUnsignedDouble(self.sock)

    def readUnsignedFloat(self) -> float:
        return readUnsignedFloat(self.sock)

    def readString(self) -> str:
        return readString(self.sock)


class TypeIO:
    @abc.abstractmethod
    def fromClass(self, arg: object) -> bool:
        pass

    @abc.abstractmethod
    def read(self, dis: DataInputStream) -> object:
        pass

    @abc.abstractmethod
    def write(self, dos: DataOutputStream, arg: object):
        pass


class ByteTypeIO(TypeIO):
    def fromClass(self, arg: object) -> bool:
        return isinstance(arg, bytes) or isinstance(arg, bool)

    def read(self, dis: DataInputStream) -> int:
        return dis.readByte()

    def write(self, dos: DataOutputStream, arg: Union[int, bool]):
        if isinstance(arg, bool):
            toWrite: int = 1 if arg else 0
        else:
            toWrite: int = int(arg)
        dos.writeByte(toWrite)


class DoubleTypeIO(TypeIO):
    def fromClass(self, arg: object) -> bool:
        return isinstance(object, float)

    def read(self, dis: DataInputStream) -> float:
        return dis.readDouble()

    def write(self, dos: DataOutputStream, arg: float):
        dos.writeDouble(arg)


class FloatTypeIO(TypeIO):

    def fromClass(self, arg: object) -> bool:
        return isinstance(object, float)

    def read(self, dis: DataInputStream) -> float:
        return dis.readFloat()

    def write(self, dos: DataOutputStream, arg: float):
        dos.writeFloat(arg)


class IntTypeIO(TypeIO):
    def fromClass(self, arg: object) -> bool:
        return isinstance(arg, int)

    def read(self, dis: DataInputStream) -> int:
        return dis.readInteger()

    def write(self, dos: DataOutputStream, arg: int):
        dos.writeInteger(arg)


class LongTypeIO(TypeIO):
    def fromClass(self, arg: object) -> bool:
        return isinstance(arg, int)

    def read(self, dis: DataInputStream) -> int:
        return dis.readLong()

    def write(self, dos: DataOutputStream, arg: int):
        dos.writeLong(arg)


class StringTypeIO(TypeIO):
    def fromClass(self, arg: object) -> bool:
        return isinstance(arg, str)

    def read(self, dis: DataInputStream) -> str:
        return dis.readString()

    def write(self, dos: DataOutputStream, arg: str):
        dos.writeString(arg)


class Type:
    def __init__(self, io: TypeIO, repre: str):
        self.__io: TypeIO = io
        self.__repre: str = repre

    @property
    def io(self) -> TypeIO:
        return self.__io

    @property
    def repr(self) -> str:
        return self.__repre


class Types:
    BYTE: Type = Type(ByteTypeIO(), "B")
    DOUBLE: Type = Type(DoubleTypeIO(), "D")
    FLOAT: Type = Type(FloatTypeIO(), "F")
    INTEGER: Type = Type(IntTypeIO(), "I")
    LONG: Type = Type(LongTypeIO(), "L")
    STRING: Type = Type(StringTypeIO(), "S")

    @staticmethod
    def getTypeFromRepr(repre: str) -> Union[None, Type]:
        for fieldName in list(filter(lambda x: not x.startswith("__") and not x.endswith("__"), dir(Types))):
            field: Type = getattr(Types, fieldName)
            if field.repr == repre:
                return field
        return None

    @staticmethod
    def getTypeFromArg(arg: object) -> Union[None, Type]:
        for fieldName in list(filter(lambda x: not x.startswith("__") and not x.endswith("__"), dir(Types))):
            field: Type = getattr(Types, fieldName)
            if field.io.fromClass(arg):
                return field
        return None


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

    def getPacketID(self) -> int:
        return 0x07

    def read(self, dis: DataInputStream):
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


class EventRegistry:
    events: [int, [callable]] = {}
    TO_ID = {
        ClientConnectPacket: 0x01,
        ClientDisconnectPacket: 0x02,
        InformationPacket: 0x08,
        RouteNotFoundPacket: 0x07,
        RouteResponsePacket: 0x06,
        ServerClosePacket: 0x03,
        UnauthorizedClientConnectPacket: 0x00
    }

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


# TODO: Make event decarator based on event class not id
def packet_event(packet_id):
    def decarotor(func):
        if packet_id not in EventRegistry.TO_ID:
            raise RuntimeError("There is no such a packet")
        EventRegistry._register(EventRegistry.TO_ID[packet_id], func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return decarotor


class PacketReader:
    def __init__(self, net):
        self.__net = net
        self.dis = DataInputStream(self.__net.client)

    def start(self):
        threading.Thread(target=self.__read_packets_until_shutdown, daemon=True).start()

    def __read_packets_until_shutdown(self):
        Printer.print("Starting reading network")
        while self.__net.isRunning:
            try:
                Printer.print("Waitin for id")
                packetID: int = self.dis.readInteger()
                packet: Packet = PacketFactory.getPacketFromID(packetID)
                Printer.print("id found: "+str(packetID))
                if packet is not None:
                    packet.read(self.dis)
                    EventRegistry.fireEvent(self.__net, packetID, packet)
            except InterruptedError as e:
                self.__net.reconnect()
                Printer.print("Err ")
                Printer.print(e)
                continue


class PacketSender:
    def __init__(self, net):
        self.__net = net
        self.__packet_queue = Queue()

    def start(self):
        threading.Thread(target=self.__send_packets_until_shutdown, daemon=True).start()

    def addPacket(self, packet):  # TODO: typing
        self.__packet_queue.put(packet)

    def __send_packets_until_shutdown(self):
        Printer.print("Starting Packet Sender")
        while self.__net.isRunning:
            try:
                packet: Packet = self.__packet_queue.get()
                Printer.print("sending packet "+str(packet))
                dos: DataOutputStream = DataOutputStream(self.__net.client)
                packet.write(dos)
            except InterruptedError:
                self.__net.reconnect()
                return


class Network:
    def __init__(self, ip: str, port: int, authKey: str):
        self.ip: str = ip
        self.port: int = port
        self.authKey: str = authKey

        self.client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(True)
        self.client_id = None

        self.__isRunning: bool = False

        self.__isAuthorized = False  # Make a

        self.__packet_sender: PacketSender = PacketSender(self)
        self.__packet_reader: PacketReader = PacketReader(self)

        self.__callbacks: [int, callable] = {}
        self.__request_counter: int = 0

    @property
    def isRunning(self) -> bool:
        return self.__isRunning

    @property
    def callbacks(self):
        return self.__callbacks

    def start(self):
        self.client.settimeout(10.0)
        self.__connect_until_response()
        self.client.settimeout(None)
        self.__packet_sender.start()
        self.__packet_reader.start()

        auth = AuthorizationPacket()
        auth.authKey = self.authKey
        self.sendPacket(auth)

    def reconnect(self):
        self.__isRunning = False
        self.start()

    def sendPacket(self, packet: Packet):
        self.__packet_sender.addPacket(packet)

    def request(self, route_name: str, callback: callable, *args):
        requestPacket: RouteRequestPacket = RouteRequestPacket()
        requestPacket.route_name = route_name
        requestPacket.args = list(args)
        self.sendPacket(requestPacket)
        self.__callbacks[self.__request_counter] = callback
        self.__request_counter += 1

    def removeFromCallback(self, rid: int):
        self.__callbacks.pop(rid)

    def __connect_until_response(self):
        while not self.isRunning:
            try:
                self.client.connect((self.ip, self.port))
                self.__isRunning = True
            except TimeoutError:
                self.__isRunning = False
                continue


@packet_event(InformationPacket)
def information_handler(network: Network, packet: InformationPacket):
    network.client_id = packet.client_id


@packet_event(RouteNotFoundPacket)
def route_not_found(network: Network, packet: RouteNotFoundPacket):
    raise RuntimeError("No route found with the name of " + packet.route_name)


@packet_event(RouteResponsePacket)
def route_response_packet(network: Network, packet: RouteResponsePacket):
    network.callbacks[packet.response_id](packet.arg)
    network.removeFromCallback(packet.response_id)
