from core.packets.Packet import Packet


class PacketFactory:
    packets: [int, callable] = {}

    @staticmethod
    def registerPacket(packetID: int, supplier: callable):
        PacketFactory.packets[packetID] = supplier

    @staticmethod
    def getPacketFromID(ID: int) -> Packet:
        return PacketFactory.packets[ID]()


# TODO: Register Incoming Packets