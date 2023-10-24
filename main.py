from network import *
net = Network("localhost", 8080, "kutup is awesomez")
net.start()

while True:
    cmd = input("> ")
    if cmd == "siktir": break
    lis = net.request_blocking(cmd)
    print(lis)
net.client.close()
