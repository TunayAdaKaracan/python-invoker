from abc import abstractmethod
from utils.DataStream import DataOutputStream, DataInputStream
from typing import Union


class TypeIO:
    @abstractmethod
    def fromClass(self, arg: object) -> bool:
        pass

    @abstractmethod
    def read(self, dis: DataInputStream) -> object:
        pass

    @abstractmethod
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
    def __init__(self, io: TypeIO, repr: str):
        self.__io: TypeIO = io
        self.__repr: str = repr

    @property
    def io(self) -> TypeIO:
        return self.__io

    @property
    def repr(self) -> str:
        return self.__repr


class Types:
    BYTE: Type = Type(ByteTypeIO(), "B")
    DOUBLE: Type = Type(DoubleTypeIO(), "D")
    FLOAT: Type = Type(FloatTypeIO(), "F")
    INTEGER: Type = Type(IntTypeIO(), "I")
    LONG: Type = Type(LongTypeIO(), "L")
    STRING: Type = Type(StringTypeIO(), "S")

    @staticmethod
    def getTypeFromRepr(repr: str) -> Union[None, Type]:
        for fieldName in list(filter(lambda x: not x.startswith("__") and not x.endswith("__"), dir(Types))):
            field: Type = getattr(Types, fieldName)
            if field.repr == repr:
                return field
        return None

    @staticmethod
    def getTypeFromArg(arg: object) -> Union[None, Type]:
        for fieldName in list(filter(lambda x: not x.startswith("__") and not x.endswith("__"), dir(Types))):
            field: Type = getattr(Types, fieldName)
            if field.io.fromClass(arg):
                return field
        return None