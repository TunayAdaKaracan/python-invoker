import threading
import socket
import uuid
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


class EventRegistry:
    def __init__(self):
        self.events: [int, [callable]] = {}

    def _register(self, packet_id: int, event: callable):
        if packet_id not in self.events:
            self.events[packet_id] = []

        self.events[packet_id].append(event)

    def fireEvent(self, network, packet_id: int, packet: Packet):
        if packet_id in self.events:
            for event in self.events[packet_id]:
                event(network, packet)

    @staticmethod
    def findIDFromClass(cls):
        for id, clazz in PacketFactory.packets.items():
            if cls == clazz:
                return id
        return None


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
                    self.__net._event_registry.fireEvent(self.__net, packetID, packet)
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
    def __init__(self, ip: str, port: int, authKey: str, custom_packets=None):

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
        self.__custom_packets = custom_packets or []

        self._event_registry = EventRegistry()

        # Default Event Funcs
        self._event_registry._register(EventRegistry.findIDFromClass(InformationPacket), self.information_handler)
        self._event_registry._register(EventRegistry.findIDFromClass(RouteNotFoundPacket), self.route_not_found)
        self._event_registry._register(EventRegistry.findIDFromClass(RouteResponsePacket), self.route_response_packet)
        self._event_registry._register(EventRegistry.findIDFromClass(ServerRejectedClientPacket), self.client_rejected)
        self._event_registry._register(EventRegistry.findIDFromClass(RouteInvokeErrorPacket), self.route_error)

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

        for customPacket in self.__custom_packets:
            packet = EnableCustomPacketPacket()
            packet.packet_id = customPacket
            self.sendPacket(packet)

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
        random_uuid = uuid.uuid4()
        requestPacket: RouteRequestPacket = RouteRequestPacket()
        requestPacket.uuid = random_uuid
        requestPacket.route_name = route_name
        requestPacket.args = list(args)
        self.sendPacket(requestPacket)
        self.__callbacks[str(random_uuid)] = callback
        self.__request_counter += 1

    def request_blocking(self, route_name: str, *args):
        ret_val = None
        event = threading.Event()

        def internal_call(value):
            nonlocal ret_val
            ret_val = value
            event.set()

        self.request(route_name, internal_call, *args)

        event.wait()
        return ret_val

    def removeFromCallback(self, rid):
        self.__callbacks.pop(rid)

    def __connect_until_response(self):
        while not self.isRunning:
            try:
                self.client.connect((self.ip, self.port))
                self.__isRunning = True
            except TimeoutError:
                self.__isRunning = False
                continue

    def packet_event(self, packet_class):
        def decorator(func):
            if EventRegistry.findIDFromClass(packet_class) is None:
                raise RuntimeError("There is no such a packet")
            self._event_registry._register(EventRegistry.findIDFromClass(packet_class), func)
            def wrapper(*args, **kwargs):
                func(*args, **kwargs)

            return wrapper

        return decorator

    # Default Behaviours

    def information_handler(self, net, packet: InformationPacket):
        self.client_id = packet.client_id

    def route_not_found(self, net, packet: RouteNotFoundPacket):
        raise RuntimeError("No route found. Request ID: "+str(packet.route_id) +" Route Name:"+packet.route_name)

    def client_rejected(self, net, packet: ServerRejectedClientPacket):
        self.close()
        raise RuntimeError("Server rejected this client.")

    def route_error(self, net, packet: RouteInvokeErrorPacket):
        raise RuntimeError("Error on "+packet.route_name+" with request uuid of "+str(packet.route_id)+":"+packet.error_message)

    def route_response_packet(self, net, packet: RouteResponsePacket):
        self.callbacks[str(packet.response_id)](packet.arg)
        self.removeFromCallback(str(packet.response_id))