import time
import subprocess

proceso = subprocess.Popen(['tshark', '-d', 'tcp.port==8081'])

time.sleep(10)

proceso.kill()