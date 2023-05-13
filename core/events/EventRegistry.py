from core.net.Network import Network
from core.packets.Packet import Packet


class EventRegistry:
    events: [int, [callable]] = {}

    @staticmethod
    def _register(packet_id: int, event: callable):
        if packet_id not in EventRegistry.events:
            EventRegistry.events[packet_id] = []

        EventRegistry.events[packet_id].append(event)

    @staticmethod
    def fireEvent(packet_id: int, packet: Packet):
        if packet_id in EventRegistry.events:
            for event in EventRegistry.events[packet_id]:
                event(Network.instance.client, packet)


def packet_event(packet_id: int):
    def decarotor(func):
        EventRegistry._register(packet_id, func)

        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    return decarotor