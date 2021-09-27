import scapy.all as scapy
from scapy.layers.l2 import Ether

def procesar_paquete(x):
    print(type(x))
    print(x.mysummary())
    print(x.payload_guess)

scapy.sniff(count=100, iface="ens33", prn=procesar_paquete)