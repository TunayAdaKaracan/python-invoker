from core.net.Network import Network
from core.packets.Packet import Packet
from core.packets.incoming import *


class EventRegistry:
    events: [int, [callable]] = {}
    TO_ID = {
        ClientConnectPacket: 0x01,
        ClientDisconnectPacket: 0x02,
        InformationPacket: 0x08,
        RouteNotFoundPacket: 0x07,
        RouteResponsePacket: 0x06,
        ServerClosePacket: 0x03,
        UnauthorizedClientConnectPacket: 0x00
    }

    @staticmethod
    def _register(packet_id: int, event: callable):
        if packet_id not in EventRegistry.events:
            EventRegistry.events[packet_id] = []

        EventRegistry.events[packet_id].append(event)

    @staticmethod
    def fireEvent(packet_id: int, packet: Packet):
        if packet_id in EventRegistry.events:
            for event in EventRegistry.events[packet_id]:
                event(Network.instance, packet)



# TODO: Make event decarator based on event class not id
def packet_event(packet_id):
    def decarotor(func):
        if packet_id not in EventRegistry.TO_ID:
            raise RuntimeError("There is no such a packet")
        EventRegistry._register(EventRegistry.TO_ID[packet_id], func)

        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return decarotor


@packet_event(InformationPacket)
def information_handler(network: Network, packet: InformationPacket):
    network.client_id = packet.client_id


@packet_event(RouteNotFoundPacket)
def route_not_found(network: Network, packet: RouteNotFoundPacket):
    raise RuntimeError("No route found with the name of "+packet.route_name)


@packet_event(RouteResponsePacket)
def route_response_packet(network: Network, packet: RouteResponsePacket):
    pass # TODO