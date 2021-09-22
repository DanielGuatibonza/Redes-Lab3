from concurrent.futures import ThreadPoolExecutor, as_completed
import socket, sys
# s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
from settings import *

'''
while True:
    print ('Listening at', s.getsockname())
    sc, sockname = s.accept()
    print ('We have accepted a connection from', sockname)
    print ('Socket connects', sc.getsockname(), 'and', sc.getpeername())
    message = recv_all(sc, 16)
    print ('The incoming sixteen-octet message says.py', repr(message))
    sc.sendall('Farewell client.'.encode())
    sc.close()
    print ('Reply sent, socket closed.')
'''

sockets_clientes = []

tamano_archivo = input ("Ingrese el tamaño del archivo que requiere (MB): ")
nombre_archivo = 'ArchivosServidor/file' + tamano_archivo + '.txt'
num_clientes = input ('Ingrese el número de clientes que solicitan el archivo: ')
num_clientes = num_clientes if len(num_clientes) > 1 else "0" + num_clientes

s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(25)
print ('Escuchando en', s.getsockname())
sc, sockname = s.accept()
sc.sendall((num_clientes + ',' + tamano_archivo).encode())

def iniciar_protocolo():
    sc, sockname = s.accept()
    print ('Se ha aceptado una conexión de', sockname)
    print ('El socket se conecta desde', sc.getsockname(), 'hacia', sc.getpeername())
    message = recv_all(sc, len(CLIENTE_LISTO))
    print ('El mensaje entrante dice', repr(message))
    sc.sendall(CLIENTE_ACEPTADO.encode())
    sockets_clientes.append(sc)
    if len(sockets_clientes) == num_clientes:
        for socket_cliente in sockets_clientes:
            f = open(nombre_archivo, "rb")
            l = f.read(1024)
            while (l):
                socket_cliente.send(l)
                l = f.read(1024)
            ack = recv_all(socket_cliente, len(ARCHIVO_RECIBIDO))
            print('El cliente ' + socket_cliente.getpeername() + ' respondió ' + ack)

with ThreadPoolExecutor(max_workers=25) as pool:
    futures = {pool.submit(iniciar_protocolo) for _ in range(25)}
    for fut in as_completed(futures):
        print(f"La salida es {fut.result()}")