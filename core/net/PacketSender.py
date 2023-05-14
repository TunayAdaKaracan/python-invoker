import threading
from queue import Queue
from core.net.Network import Network
from core.packets.Packet import Packet
from utils.DataStream import DataOutputStream


class PacketSender:
    def __init__(self, net: Network):
        self.__net = net
        self.__packet_queue = Queue()

    def start(self):
        threading.Thread(target=self.__send_packets_until_shutdown, daemon=True).start()

    def addPacket(self, packet): # TODO: typing
        self.__packet_queue.put(packet)

    def __send_packets_until_shutdown(self):
        while self.__net.isRunning:
            try:
                packet: Packet = self.__packet_queue.get()
                dos: DataOutputStream = DataOutputStream(self.__net.client)
                packet.write(dos)
            except InterruptedError:
                self.__net.reconnect()
                return