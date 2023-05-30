from network import *
net = Network("localhost", 8080, "kutup is awesome")
net.start()


@packet_event(InformationPacket)
def inf(network, packet: InformationPacket):
    print("I am client "+ str(packet.client_id))


while True:
    cmd = input("> ")
    if cmd == "active":
        net.request("kutup_isActive", lambda v: print(v), "Kutup_Tilkisi")
    elif cmd == "echo":
        net.request("kutup_echo", lambda v: print(v), "Hi!")
    elif cmd == "close":
        break

net.client.close()