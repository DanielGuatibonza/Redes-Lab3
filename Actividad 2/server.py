from concurrent.futures import ThreadPoolExecutor, as_completed
import socket, hashlib, subprocess, time, logging
from datetime import datetime
from settings import *

addresses = {}

tamano_archivo = input ('Ingrese el tamaño del archivo que requiere (MB): ')
file_name = 'ArchivosServidor/file' + tamano_archivo + '.txt'
num_clientes = input('Ingrese el número de clientes que solicitan el archivo: ')
num_clientes = num_clientes if len(num_clientes) > 1 else '0' + num_clientes

formated_date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
logging.basicConfig(filename='Logs/Servidor/'+formated_date +'-log.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger('Logs/Servidor/'+formated_date +'-log')
log.setLevel(logging.DEBUG)
log.debug('Archivo a enviar: ' + file_name + ', Tamaño: ' + tamano_archivo + 'MB.')

archivo_captura = open('capturaTshark.txt', 'wb')
txt_captura = subprocess.Popen(['tshark'], stdout=archivo_captura)
pcap_captura = subprocess.Popen(['tshark', '-i', 'ens33', '-w', 'traff.pcap', '-F', 'pcap'])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
s.listen(25)
print ('Escuchando en', s.getsockname())
data, clientAddr = s.recvfrom(SOLICITAR_CONEXION)
s.sendto(((num_clientes + ',' + tamano_archivo).encode()), clientAddr)

def iniciar_protocolo():
    global addresses
    data, clientAddr = s.recvfrom(len(CLIENTE_LISTO)+3)
    print ('Se ha aceptado una conexión de', str(clientAddr))
    print ('El socket se conecta desde', (HOST, PORT), 'hacia', str(clientAddr))
    log.debug('Se realizó la conexión con el cliente: ' + str(clientAddr))
    print('El mensaje entrante dice', str(data))
    s.sendto(CLIENTE_ACEPTADO.encode(), clientAddr)
    addresses[data.split(':')[1]] = clientAddr
    return len(addresses)

def enviar_archivo(client_address):
    global file_name
    tiempo_inicio = time.time()
    with open(file_name, 'rb') as f:
        l = f.read(4096)
        while (l):
            client_address.send(l)
            l = f.read(4096)
    with open(file_name, 'r') as f:
        data = f.read()
        hash_data = hashlib.sha256(data.encode()).hexdigest()
        client_address.send(hash_data.encode())
        ack = recv_all(client_address, len(ARCHIVO_RECIBIDO))
        print('El cliente ' + str(client_address.getpeername()) + ' respondió: ' + ack)
        log.debug('El cliente ' + str(client_address.getpeername()) + ' respondió: ' + ack)
    log.debug('El tiempo de transferencia del archivo al cliente ' + str(client_address.getpeername()) + ' fue de ' + str(time.time() - tiempo_inicio) + ' segundos.')
    client_address.close()
    return ack

with ThreadPoolExecutor(max_workers=25) as pool:
    futures = {pool.submit(iniciar_protocolo) for _ in range(int(num_clientes))}
    for fut in as_completed(futures):
        print(f'La salida es {fut.result()}')
    futures = {pool.submit(enviar_archivo, client_address) for client_address in addresses.values()}
    for fut in as_completed(futures):
        print(f'El resultado del envío del archivo fue: {fut.result()}')

txt_captura.kill()
pcap_captura.kill()

archivo_filtrado = open('filtroTshark.txt', 'wb')
proceso_filtro = subprocess.Popen(['tshark', '-r', 'traff.pcap', '-Y', 'tcp.analysis.retransmission'], stdout=archivo_filtrado)
time.sleep(5)
proceso_filtro.kill()

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

with open('filtroTshark.txt', 'r') as archivo_filtrado:
    paquetes_retransmitidos = 0
    bytes_retransmitidos = 0
    for linea in archivo_filtrado:
        partes = linea.split()
        bytes_retransmitidos += int(partes[6])
        paquetes_retransmitidos += 1
    log.info('El número de paquetes retransmitidos fue: ' + str(paquetes_retransmitidos))
    sc_principal.sendall(('{:10d},{:10d},{:8d},{:8d}'.format(num_bytes_SC, bytes_retransmitidos, num_paquetes_SC, paquetes_retransmitidos)).encode())
sc_principal.close()
s.close()