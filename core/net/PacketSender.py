import socket
import threading
from queue import Queue
from core.net.Network import Network

# Actual implementation
class PacketSender:
    def __init__(self, net: "Network"):
        self.net = net
        self.packet_queue = Queue()

    def addPacket(self, packet): # TODO: typing
        self.packet_queue.put(packet)

    def __send_packets_until_shutdown(self):
        while self.net.isRunning:
            packet = self.packet_queue.get()