from core.packets.Packet import Packet
from core.packets.incoming import *
from typing import Union


class PacketFactory:
    packets: [int, callable] = {}

    @staticmethod
    def registerPacket(packetID: int, supplier: callable):
        PacketFactory.packets[packetID] = supplier

    @staticmethod
    def getPacketFromID(ID: int) -> Union[None, Packet]:
        if ID not in PacketFactory.packets:
            return None
        return PacketFactory.packets[ID]()


# TODO: Register Incoming Packets
PacketFactory.registerPacket(ClientConnectPacket().getPacketID(), ClientConnectPacket.__init__)
PacketFactory.registerPacket(ClientDisconnectPacket().getPacketID(), ClientDisconnectPacket.__init__)
PacketFactory.registerPacket(InformationPacket().getPacketID(), InformationPacket.__init__)
PacketFactory.registerPacket(RouteNotFoundPacket().getPacketID(), RouteNotFoundPacket.__init__)
PacketFactory.registerPacket(RouteResponsePacket().getPacketID(), RouteResponsePacket.__init__)
PacketFactory.registerPacket(ServerClosePacket().getPacketID(), ServerClosePacket.__init__)
PacketFactory.registerPacket(UnauthorizedClientConnectPacket().getPacketID(), UnauthorizedClientConnectPacket.__init__)