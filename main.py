import time
import sys
from network import *

net = Network("localhost", 8080, "kutup is awesome")


@net.packet_event(InformationPacket)
def a(net, pack):
    print("I am client: "+pack.client_id)


net.start()
input("> ")
net.client.close()