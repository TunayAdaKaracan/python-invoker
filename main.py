from invoker import Network, packet_event, InformationPacket, ClientConnectPacket, Printer

net = Network("localhost", 8080, "kutup is awesome")
net.start()


@packet_event(InformationPacket)
def event(net: Network, packet: InformationPacket):
    Printer.print("I am client "+str(packet.client_id))


@packet_event(ClientConnectPacket)
def clientConnect(net: Network, packet: ClientConnectPacket):
    Printer.print("Client connected with id of: "+str(packet.client_id))


while True:
    cmd = input("Cmd: ")
    if cmd == "request":
        net.request("kutup_echo", lambda b: print(b), "Kutup_Tilkisi")