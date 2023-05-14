import threading
from core.net.Network import Network
from utils.DataStream import DataInputStream
from core.packets import Packet, PacketFactory
from core.events.EventRegistry import EventRegistry


class PacketReader:
    def __init__(self, net: Network):
        self.__net: Network = net
        self.dis = DataInputStream(self.__net.client)

    def start(self):
        threading.Thread(target=self.__read_packets_until_shutdown, daemon=True).start()

    def __read_packets_until_shutdown(self):
        while self.__net.isRunning:
            try:
                packetID: int = self.dis.readInteger()
                packet: Packet = PacketFactory.getPacketFromID(packetID)
                if packet is not None:
                    packet.read(self.dis)
                    EventRegistry.fireEvent(packetID, packet)
            except InterruptedError:
                self.__net.reconnect()
                return