from utils.WriterUtils import *
from utils.ReaderUtils import *


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