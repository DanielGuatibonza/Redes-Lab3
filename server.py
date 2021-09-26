from concurrent.futures import ThreadPoolExecutor, as_completed
import socket, sys
from settings import *
import hashlib, pyshark

sockets_clientes = {}

tamano_archivo = input ("Ingrese el tamaño del archivo que requiere (MB): ")
nombre_archivo = 'ArchivosServidor/file' + tamano_archivo + '.txt'
num_clientes = input('Ingrese el número de clientes que solicitan el archivo: ')
num_clientes = num_clientes if len(num_clientes) > 1 else "0" + num_clientes

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s.bind((HOST, PORT))
s.listen(25)
print ('Escuchando en', s.getsockname())
sc, sockname = s.accept()
sc.sendall((num_clientes + ',' + tamano_archivo).encode())

def capturar_paquetes():
    capture = pyshark.LiveCapture(interface='ens33', bpf_filter='ip.src == '+HOST)
    for pk in capture.sniff_continuously():
        print(pk)
    return capture

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

def enviar_archivo(socket_cliente):
    global nombre_archivo
    with open(nombre_archivo, "rb") as f:
        l = f.read(1024)
        while (l):
            socket_cliente.send(l)
            l = f.read(1024)
    with open(nombre_archivo, "r") as f:
        data = f.read()
        hash_data = hashlib.sha256(data.encode()).hexdigest()
        socket_cliente.send(hash_data.encode())
        ack = recv_all(socket_cliente, len(ARCHIVO_RECIBIDO))
        print('El cliente ' + str(socket_cliente.getpeername()) + ' respondió: ' + ack)
    socket_cliente.close()
    return ack

paquetes = None
with ThreadPoolExecutor(max_workers=25) as pool:
    captura = {pool.submit(capturar_paquetes)}
    futures = {pool.submit(iniciar_protocolo) for _ in range(int(num_clientes))}
    for fut in as_completed(futures):
        print(f"La salida es {fut.result()}")
    futures = {pool.submit(enviar_archivo, socket_cliente) for socket_cliente in sockets_clientes.values()}
    for fut in as_completed(futures):
        print(f"El resultado del envío del archivo fue: {fut.result()}")
    for cap in as_completed(captura):
        # paquetes = cap.result()._packets
        print(f"El resultado de la captura fue: {cap.result()}")
        for paquete in cap.result():
            print(paquete)
