import socket, sys
from settings import *
from concurrent.futures import ThreadPoolExecutor, as_completed


def recibir_archivo(i):
    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    s.connect ((HOST, PORT))
    print ('Al cliente {} le fue asignado el socket con nombre {}'.format(i, s.getsockname()))
    s.sendall ('Actualmente me encuentro activo para recibir archivos.'.encode())
    reply = recv_all (s, 16)
    print ('The server said', repr(reply))
    s.close()

s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
s.connect ((HOST, PORT))
num_clientes = int(recv_all (s, 2))
print(num_clientes)
s.close()

with ThreadPoolExecutor(max_workers=25) as pool:
    futures = {pool.submit(recibir_archivo, i) for i in range(num_clientes)}

    for fut in as_completed(futures):
        print(f"El resultado es {fut.result()}")