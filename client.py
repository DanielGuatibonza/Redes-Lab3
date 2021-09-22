import socket, sys
from settings import *
from concurrent.futures import ThreadPoolExecutor, as_completed

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
reply = recv_all(s, 6)
num_clientes = int(reply.split(',')[0])
tamano_archivo = int(reply.split(',')[1])
print(num_clientes)
s.close()

def recibir_archivo(i):
    global tamano_archivo, num_clientes
    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    s.connect ((HOST, PORT))
    print('Al cliente {} le fue asignado el socket con nombre {}'.format(i, s.getsockname()))
    identificador = str(i) if i >= 10 else '0'+str(i)
    s.sendall((CLIENTE_LISTO+':'+identificador).encode())
    reply = recv_all(s, len(CLIENTE_ACEPTADO))
    print('El servidor respondió con', repr(reply))
    file_data = recv_all(s, tamano_archivo)
    with open('ArchivosRecibidos/Cliente{}-Prueba-{}.txt'.format(i, num_clientes), 'w') as archivo:
        archivo.write(file_data)
    s.sendall(ARCHIVO_RECIBIDO.encode())
    s.close()
    return len(file_data)

with ThreadPoolExecutor(max_workers=25) as pool:
    futures = {pool.submit(recibir_archivo, i+1) for i in range(num_clientes)}
    for fut in as_completed(futures):
        print(f"El resultado es {fut.result()}")