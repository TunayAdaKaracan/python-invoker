import socket
import struct


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
    writeBytes(sock, struct.pack(">H", int))


def writeUnsignedInteger(sock: socket.socket, v: int):
    writeBytes(sock, struct.pack(">I", v))


def writeUnsignedDouble(sock: socket.socket, v: float):
    writeBytes(sock, struct.pack(">D", v))


def writeUnsignedFloat(sock: socket.socket, v: float):
    writeBytes(sock, struct.pack(">F", v))


def writeUnsignedLong(sock: socket.socket, v: int):
    writeBytes(sock, struct.pack(">L", v))


def writeString(sock: socket.socket, v: str):
    writeBytes(sock, struct.pack(">H", len(v))+v.encode("utf-8"))