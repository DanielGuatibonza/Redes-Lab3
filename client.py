import socket, sys
from settings import *
from concurrent.futures import ThreadPoolExecutor

HOST = input ('Ingrese la dirección IP del servidor: ')
PORT = input ('Ingrese el puerto del servidor: ')
num_clientes = int(input('Ingrese el número de clientes a generar: '))

def recibir_archivo(i):
    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    s.connect ((HOST, PORT))
    print ('Al cliente {} le fue asignado el socket con nombre {}'.format(i, s.getsockname()))
    s.sendall ('Toy listo.'.encode())
    reply = recv_all (s, 16)
    print ('The server said', repr(reply))
    s.close()

pool = ThreadPoolExecutor(max_workers=25)
for i in range(num_clientes):
    pool.submit(recibir_archivo, i+1)