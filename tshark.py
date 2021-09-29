import subprocess
import time

archivo_captura = open('capturaTshark.txt', 'wb')
proceso_captura = subprocess.Popen(['tshark'], stdout=archivo_captura)
pcap_captura = subprocess.Popen(['tshark', '-i', 'ens33', '-w', 'traff.pcap', '-F', 'pcap'], stdout=archivo_captura)

time.sleep(15)
proceso_captura.close()
pcap_captura.close()

archivo_filtrado = open('filtroTshark.txt', 'wb')
proceso = subprocess.Popen(['tshark', '-r', 'traff.pcap', '-Y', 'tcp.analysis.retransmission'], stdout=archivo_filtrado)

time.sleep(15)
proceso.close()