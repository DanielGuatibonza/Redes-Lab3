import socket

s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))#, socket.IPPROTO_TCP)
bytes_ = []
while True:
    bytes_.append(len(s.recvfrom(65565)))
    print("Suma", sum(bytes_)) 
    print("Paquetes", len(bytes_)) 