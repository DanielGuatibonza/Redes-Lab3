import socket

s = socket.socket(socket.AF_INET, socket.SOCK_RAW)#, socket.IPPROTO_TCP)
bytes_ = []
while True:
    bytes_.append(len(s.recvfrom(65565)))
    print("Suma", sum(bytes_)) 
    print("Paquetes", len(bytes_)) 