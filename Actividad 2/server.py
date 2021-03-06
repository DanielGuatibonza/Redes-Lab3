from concurrent.futures import ThreadPoolExecutor, as_completed
import socket
import hashlib
import subprocess
import time
import logging
from datetime import datetime
from settings import *

addresses = {}
correct_clients = []
incorrect_clients = []

tamano_archivo = input('Ingrese el tamaño del archivo que requiere (MB): ')
file_name = 'ArchivosServidor/file' + tamano_archivo + '.txt'
num_clientes = input(
    'Ingrese el número de clientes que solicitan el archivo: ')
num_clientes = num_clientes if len(num_clientes) > 1 else '0' + num_clientes

formated_date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
logging.basicConfig(filename='Logs/Servidor/'+formated_date + '-log.log',
                    filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger('Logs/Servidor/'+formated_date + '-log')
log.setLevel(logging.DEBUG)
log.debug('Archivo a enviar: ' + file_name +
          ', Tamaño: ' + tamano_archivo + 'MB.')

archivo_captura = open('capturaTshark.txt', 'wb')
txt_captura = subprocess.Popen(['tshark'], stdout=archivo_captura)
pcap_captura = subprocess.Popen(
    ['tshark', '-i', 'ens33', '-w', 'traff.pcap', '-F', 'pcap'])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
print('Escuchando en', s.getsockname())
data, main_client = s.recvfrom(CHUNKS_SIZE)
s.sendto(((num_clientes + ',' + tamano_archivo).encode()), main_client)


def iniciar_protocolo():
    global s, addresses
    data, clientAddr = s.recvfrom(CHUNKS_SIZE)
    print('Se ha aceptado una conexión de', str(clientAddr))
    print('El socket se conecta desde', (HOST, PORT), 'hacia', str(clientAddr))
    log.debug('Se realizó la conexión con el cliente: ' + str(clientAddr))
    print('El mensaje entrante dice: ', str(data.decode()))
    s.sendto(CLIENTE_RECONOCIDO.encode(), clientAddr)
    addresses[data.decode().split(':')[1]] = clientAddr
    return len(addresses)


def enviar_archivo(client_address):
    global s, file_name
    tiempo_inicio = time.time()
    with open(file_name, 'rb') as f:
        l = f.read(CHUNKS_SIZE)
        while (l):
            s.sendto(l, client_address)
            l = f.read(CHUNKS_SIZE)
    with open(file_name, 'r') as f:
        data = f.read()
        hash_data = hashlib.sha256(data.encode()).hexdigest()
        s.sendto(hash_data.encode(), client_address)
        ack, client_address = s.recvfrom(CHUNKS_SIZE)
        print('El mensaje entrante dice: ', ack.decode())
        log.debug("El cliente " + str(client_address) +
                  " indicó: " + ack.decode())
        partes = ack.decode().split(":")
        print(partes)
        if partes[0] == ARCHIVO_RECIBIDO:
            correct_clients.append(partes[1] + " " + str(client_address))
        elif partes[0] == ARCHIVO_INCORRECTO:
            incorrect_clients.append(partes[1] + " " + str(client_address))
    log.debug('El tiempo de transferencia del archivo al cliente ' +
              str(client_address) + ' fue de ' + str(time.time() - tiempo_inicio) + ' segundos.')
    return ack


with ThreadPoolExecutor(max_workers=25) as pool:
    futures = {pool.submit(iniciar_protocolo)
               for _ in range(int(num_clientes))}
    for fut in as_completed(futures):
        print(f'El número de clientes actual es: {fut.result()}')
    futures = {pool.submit(enviar_archivo, client_address)
               for client_address in addresses.values()}
    for fut in as_completed(futures):
        print(f'El resultado del envío del archivo fue: {fut.result()}')
txt_captura.kill()
pcap_captura.kill()

for client in correct_clients:
    log.debug('El cliente ' + client + ' recibió correctamente el archivo.')
for client in incorrect_clients:
    log.debug('El cliente ' + client + ' no recibió correctamente el archivo.')

num_bytes_SC = 0
num_paquetes_SC = 0
with open('capturaTshark.txt', 'r') as archivo_completo:
    for linea in archivo_completo:
        partes = linea.split()
        if HOST + ' → ' + CLIENT_HOST in linea:
            num_bytes_SC += int(partes[6])
            num_paquetes_SC += 1
    log.info('El número de paquetes enviados fue: ' + str(num_paquetes_SC))
    log.info('El número de bytes enviados fue: ' + str(num_bytes_SC))

s.close()
