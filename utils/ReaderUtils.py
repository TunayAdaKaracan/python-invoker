import socket
import struct


def readNByte(sock: socket.socket, n: int) -> bytes:
    return sock.recv(n)


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
    len = readUnsignedShort(sock)
    return readNByte(sock, len).decode("utf-8")