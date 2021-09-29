import time
import subprocess

archivo_captura = open('capturaTshark.txt', 'wb')
proceso = subprocess.Popen(['tshark'], stdout=archivo_captura)

time.sleep(10)

proceso.kill()