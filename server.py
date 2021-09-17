import socket, sys
s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
from settings import *

HOST = sys.argv.pop() if len(sys.argv) == 3 else '127.0.0.1'

s.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))

# Input
s.listen(1)

while True:
    print ('Listening at', s.getsockname())
    sc, sockname = s.accept()
    print ('We have accepted a connection from', sockname)
    print ('Socket connects', sc.getsockname(), 'and', sc.getpeername())
    message = recv_all (sc, 16)
    print ('The incoming sixteen-octet message says.py', repr(message))
    sc.sendall('Farewell client.'.encode())
    sc.close()
    print ('Reply sent, socket closed.')

