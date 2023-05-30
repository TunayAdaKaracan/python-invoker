import abc
from datastream import DataInputStream, DataOutputStream
from typing import Union

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

