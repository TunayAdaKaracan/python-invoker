import abc
from utils.DataStream import DataInputStream, DataOutputStream
from core.net.Network import Network


class Packet(abc.ABC):
    @abc.abstractmethod
    def getPacketID(self) -> int:
        pass

    def write(self, dos: DataOutputStream):
        dos.writeInteger(self.getPacketID())

    def read(self, dis: DataInputStream):
        pass

    def send(self):
        Network.instance.sendPacket(self)