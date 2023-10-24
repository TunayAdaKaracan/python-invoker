from network import *
net = Network("localhost", 8080, "kutup is awesome", [0x0B])
net.start()


class PlayerChatPacket(Packet):
    def __init__(self):
        self.username = ""
        self.message = ""

    def getPacketID(self) -> int:
        return 0x0B

    def read(self, dis: DataInputStream):
        self.username = dis.readString()
        self.message = dis.readString()


PacketFactory.registerPacket(PlayerChatPacket().getPacketID(), PlayerChatPacket)


@packet_event(PlayerChatPacket)
def playerchatEvent(network: Network, packet: PlayerChatPacket):
    print(f"Player {packet.username}: {packet.message}")


while True:
    pass


net.client.close()