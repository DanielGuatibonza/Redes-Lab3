import scapy.all as scapy
from scapy.all import TCP
from scapy.layers.l2 import Ether

bytes_ = []
cont = 0
def procesar_paquete(paquete):
    global bytes_, cont
    length = len(paquete[TCP].__bytes__())
    if length == 1514:
        cont += 1
    bytes_.append(length)
    print("Bytes", sum(bytes_))
    print("Cantidad 1514", cont)
    print("Cantidad", len(bytes_))
    # print(type(x[Ether]))
    # print(dir(x[Ether]))
    # print(x.mysummary())
    # print(x.payload_guess)

scapy.sniff(iface="ens33", prn=procesar_paquete)