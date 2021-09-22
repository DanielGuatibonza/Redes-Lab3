from concurrent.futures import ThreadPoolExecutor, as_completed
import socket, sys
from settings import *

sockets_clientes = {}

tamano_archivo = input ("Ingrese el tamaño del archivo que requiere (MB): ")
nombre_archivo = 'ArchivosServidor/file' + tamano_archivo + '.txt'
num_clientes = input('Ingrese el número de clientes que solicitan el archivo: ')
num_clientes = num_clientes if len(num_clientes) > 1 else "0" + num_clientes

s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(25)
print ('Escuchando en', s.getsockname())
sc, sockname = s.accept()
sc.sendall((num_clientes + ',' + tamano_archivo).encode())

def iniciar_protocolo():
    global sockets_clientes
    sc, sockname = s.accept()
    print ('Se ha aceptado una conexión de', sockname)
    print ('El socket se conecta desde', sc.getsockname(), 'hacia', sc.getpeername())
    message = recv_all(sc, len(CLIENTE_LISTO)+3)
    print ('El mensaje entrante dice', repr(message))
    sc.sendall(CLIENTE_ACEPTADO.encode())
    sockets_clientes[message.split(':')[1]] = sc
    return len(sockets_clientes)
        
with ThreadPoolExecutor(max_workers=25) as pool:
    futures = {pool.submit(iniciar_protocolo) for _ in range(25)}
    for fut in as_completed(futures):
        print(f"La salida es {fut.result()}")
    for socket_cliente in sockets_clientes.values():
        f = open(nombre_archivo, "rb")
        l = f.read(1024)
        while (l):
            socket_cliente.send(l)
            l = f.read(1024)
        ack = recv_all(socket_cliente, len(ARCHIVO_RECIBIDO))
        print('El cliente ' + socket_cliente.getpeername() + ' respondió ' + ack)
        socket_cliente.close()