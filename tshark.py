import time
import subprocess

proceso = subprocess.Popen(["'tshark'", '>> capturaTshark.txt'])

time.sleep(10)

proceso.kill()