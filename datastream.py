import socket
import struct
import uuid


def readNByte(sock: socket.socket, n: int) -> bytes:
    if n == 0: return b""
    data = b""
    while len(data) != n:
        data += sock.recv(n-len(data))
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
    return struct.unpack(">q", readNByte(sock, 8))[0]


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
    strlen = readInteger(sock)
    return readNByte(sock, strlen).decode("utf-8")


def readUUID(sock: socket.socket) -> uuid.UUID:
    return uuid.UUID(readNByte(sock, 16))


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
    writeBytes(sock, struct.pack(">q", v))


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
    writeBytes(sock, struct.pack(">i", len(v)) + v.encode("utf-8"))


def writeUUID(sock: socket.socket, v: uuid.UUID):
    writeBytes(sock, v.bytes)


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

    def writeUUID(self, v: uuid.UUID):
        writeUUID(self.sock, v)


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
  
    def readUUID(self) -> uuid.UUID:
        return readUUID(self.sock)