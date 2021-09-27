import scapy.all as scapy
from scapy.layers.l2 import Ether

def procesar_paquete(x):
    print(type(x))

scapy.sniff(count=100, iface="ens33", prn=procesar_paquete)