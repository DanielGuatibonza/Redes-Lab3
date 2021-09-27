import scapy.all as scapy
from scapy.all import TCP
from scapy.layers.l2 import Ether

def procesar_paquete(x):
    print(x[Ether].__bytes__())
    print(x[Ether].time)
    # print(type(x[Ether]))
    # print(dir(x[Ether]))
    # print(x.mysummary())
    # print(x.payload_guess)

scapy.sniff(iface="ens33", filter="tcp", prn=procesar_paquete)