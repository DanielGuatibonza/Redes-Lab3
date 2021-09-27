import scapy.all as scapy
from scapy.all import TCP
from scapy.layers.l2 import Ether

def procesar_paquete(x):
    x.show()
    print(type(x[TCP]))
    print(dir(x[TCP]))
    print(x[TCP].__bytes__)
    print(x[TCP].time)
    print(type(x[Ether]))
    print(dir(x[Ether]))
    # print(x.mysummary())
    # print(x.payload_guess)

scapy.sniff(iface="ens33", filter="tcp", prn=procesar_paquete)