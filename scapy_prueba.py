import scapy.all as scapy
from scapy.all import TCP
from scapy.layers.l2 import Ether

suma = 0
def procesar_paquete(x):
    global suma
    suma += len(x[Ether].__bytes__())
    print(len(x[Ether].__bytes__()))
    print(suma)
    # print(type(x[Ether]))
    # print(dir(x[Ether]))
    # print(x.mysummary())
    # print(x.payload_guess)

scapy.sniff(iface="ens33", filter="scr host 192.168.231.132", prn=procesar_paquete)