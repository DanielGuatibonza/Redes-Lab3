import scapy.all as scapy
from scapy.layers.l2 import Ether

def procesar_paquete(x):
    x.show()
    print(type(x))
    print(x.mysummary())
    print(x.payload_guess)

scapy.sniff(iface="ens33", filter="tcp", prn=procesar_paquete)