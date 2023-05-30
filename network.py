import threading
import socket
from queue import Queue
from packets import *


class Printer:
    LINES = []

    @staticmethod
    def print(any):
        #Printer.LINES.append(any)
        pass

    @staticmethod
    def _printUntilFinish():
        while True:
            if len(Printer.LINES) > 0:
                print(Printer.LINES.pop(0))

    @staticmethod
    def start():
        threading.Thread(target=Printer._printUntilFinish, daemon=True).start()


Printer.start()


class PacketReader:
    def __init__(self, net):
        self.__net = net
        self.dis = DataInputStream(self.__net.client)

    def start(self):
        threading.Thread(target=self.__read_packets_until_shutdown, daemon=True).start()

    def __read_packets_until_shutdown(self):
        Printer.print("Starting reading network")
        while self.__net.isRunning:
            try:
                Printer.print("Waitin for id")
                packetID: int = self.dis.readInteger()
                packet: Packet = PacketFactory.getPacketFromID(packetID)
                Printer.print("id found: "+str(packetID))
                if packet is not None:
                    packet.read(self.dis)
                    EventRegistry.fireEvent(self.__net, packetID, packet)
            except InterruptedError as e:
                self.__net.reconnect()
                Printer.print("Err ")
                Printer.print(e)
                continue


class PacketSender:
    def __init__(self, net):
        self.__net = net
        self.__packet_queue = Queue()

    def start(self):
        threading.Thread(target=self.__send_packets_until_shutdown, daemon=True).start()

    def addPacket(self, packet):
        self.__packet_queue.put(packet)

    def __send_packets_until_shutdown(self):
        Printer.print("Starting Packet Sender")
        while self.__net.isRunning:
            try:
                packet: Packet = self.__packet_queue.get()
                Printer.print("sending packet "+str(packet))
                dos: DataOutputStream = DataOutputStream(self.__net.client)
                packet.write(dos)
            except InterruptedError:
                self.__net.reconnect()
                return


class Network:
    def __init__(self, ip: str, port: int, authKey: str):
        self.ip: str = ip
        self.port: int = port
        self.authKey: str = authKey

        self.client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_id = None

        self.__isRunning: bool = False

        self.__isAuthorized = False

        self.__packet_sender: PacketSender = PacketSender(self)
        self.__packet_reader: PacketReader = PacketReader(self)

        self.__callbacks: [int, callable] = {}
        self.__request_counter: int = 0

    @property
    def isRunning(self) -> bool:
        return self.__isRunning

    @property
    def callbacks(self):
        return self.__callbacks

    def start(self):
        self.__connect_until_response()
        self.__packet_sender.start()
        self.__packet_reader.start()

        auth = AuthorizationPacket()
        auth.authKey = self.authKey
        self.sendPacket(auth)

    def reconnect(self):
        self.__isRunning = False
        self.client.close()
        self.start()

    def close(self):
        self.__isRunning = False
        self.client.close()

    def sendPacket(self, packet: Packet):
        self.__packet_sender.addPacket(packet)

    def request(self, route_name: str, callback: callable, *args):
        requestPacket: RouteRequestPacket = RouteRequestPacket()
        requestPacket.route_name = route_name
        requestPacket.args = list(args)
        self.sendPacket(requestPacket)
        self.__callbacks[self.__request_counter] = callback
        self.__request_counter += 1

    def removeFromCallback(self, rid: int):
        self.__callbacks.pop(rid)

    def __connect_until_response(self):
        while not self.isRunning:
            try:
                self.client.connect((self.ip, self.port))
                self.__isRunning = True
            except TimeoutError:
                self.__isRunning = False
                continue


@packet_event(InformationPacket)
def information_handler(network: Network, packet: InformationPacket):
    network.client_id = packet.client_id


@packet_event(RouteNotFoundPacket)
def route_not_found(network: Network, packet: RouteNotFoundPacket):
    raise RuntimeError("No route found. Request ID: "+str(packet.route_id) +" Route Name:"+packet.route_name)


@packet_event(ServerRejectedClientPacket)
def client_rejected(network: Network, packet: ServerRejectedClientPacket):
    network.close()
    raise RuntimeError("Server rejected this client.")


@packet_event(RouteResponsePacket)
def route_response_packet(network: Network, packet: RouteResponsePacket):
    network.callbacks[packet.response_id](packet.arg)
    network.removeFromCallback(packet.response_id)