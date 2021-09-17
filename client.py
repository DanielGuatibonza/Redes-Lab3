import socket, sys
from settings import *

s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
HOST = sys.argv.pop() if len(sys.argv) == 3 else '127.0.0.1'

s.connect ((HOST, PORT))
print ('Client has been assigned socket name.' , s.getsockname())
s.sendall ('Hi there, server.'.encode())
reply = recv_all (s, 16)
print ('The server said', repr(reply))
s.close()