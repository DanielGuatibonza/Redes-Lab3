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

tamanoArchivo = input ("Ingrese el tamaño del archivo que requiere: ")
num_clientes = input ('Ingrese el número de clientes que solicitan el archivo: ')

s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(25)
print ('Escuchando en', s.getsockname())
sc, sockname = s.accept()
sc.sendall(num_clientes.encode())

def iniciar_protocolo():
    sc, sockname = s.accept()
    print ('Se ha aceptado una conexión de', sockname)
    print ('El socket se conecta desde', sc.getsockname(), 'hacia', sc.getpeername())
    message = recv_all(sc, 16)
    print ('El mensaje entrante dice', repr(message))
    sockets_clientes.append(sc)


    sc.sendall('Hasta la vista, cliente.'.encode())
    sc.close()
    print ('Respuesta enviada, socket cerrado')

with ThreadPoolExecutor(max_workers=25) as pool:
    futures = {pool.submit(iniciar_protocolo) for _ in range(25)}

    for fut in as_completed(futures):
        print(f"La salida es {fut.result()}")