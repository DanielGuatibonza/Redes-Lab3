import time
import subprocess

proceso = subprocess.Popen(['tshark', '-d', 'tcp.port==8081', '-w', 'captura.pcap', '-F', 'pcap'])

time.sleep(10)

#proceso.kill()