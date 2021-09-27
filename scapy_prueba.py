import scapy.all as scapy
from scapy.all import TCP
from scapy.layers.l2 import Ether

bytes_ = {}
def procesar_paquete(paquete):
    bytes_.add(len(paquete[Ether].__bytes__()))
    print(bytes_)
    # print(type(x[Ether]))
    # print(dir(x[Ether]))
    # print(x.mysummary())
    # print(x.payload_guess)

scapy.sniff(iface="ens33", filter="port 8081", prn=procesar_paquete)