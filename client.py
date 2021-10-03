import socket, sys
from settings import *
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import hashlib, logging, time

formated_date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
logging.basicConfig(filename='Logs/Cliente/'+formated_date +'-log.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger('Logs/Cliente/'+formated_date +'-log')
log.setLevel(logging.DEBUG)

socket_principal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_principal.connect((HOST, PORT))
reply = recv_all(socket_principal, 6)
num_clientes = int(reply.split(',')[0])
tamano_archivo_MB = reply.split(',')[1]
tamano_archivo = 1024*1024*int(tamano_archivo_MB)
log.debug('Archivo a recibir: file' + tamano_archivo_MB + '.txt, Tamaño: ' + tamano_archivo_MB + 'MB.')

def recibir_archivo(i):
    global tamano_archivo, num_clientes
    s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    s.connect ((HOST, PORT))
    print('Al cliente {} le fue asignado el socket con nombre {}'.format(i, s.getsockname()))
    log.debug('Se conectó el cliente identificado como: ' + str(s.getsockname()))
    identificador = str(i) if i >= 10 else '0'+str(i)
    s.sendall((CLIENTE_LISTO+':'+identificador).encode())
    reply = recv_all(s, len(CLIENTE_ACEPTADO))
    print('El servidor respondió con ', repr(reply))
    tiempo_inicio = time.time()
    file_data = recv_all(s, tamano_archivo)
    log.debug('El tiempo de transferencia del archivo al cliente ' + str(s.getpeername()) + ' fue de ' + str(time.time() - tiempo_inicio) + ' segundos.')
    hash_data = hashlib.sha256(file_data.encode()).hexdigest()
    hash_server = recv_all(s, 64)
    if hash_data == hash_server:
        with open('ArchivosRecibidos/Cliente{}-Prueba-{}.txt'.format(i, num_clientes), 'w') as archivo:
            archivo.write(file_data)
        s.sendall(ARCHIVO_RECIBIDO.encode())
    else:
        s.sendall(HASH_INCORRECTO.encode())
    return s, len(file_data)

with ThreadPoolExecutor(max_workers=25) as pool:
    futures = {pool.submit(recibir_archivo, i+1) for i in range(num_clientes)}
    for fut in as_completed(futures):
        s, bytes_recibidos = fut.result()
        print(f"El tamaño del archivo recibido fue de {bytes_recibidos} bytes.")
        log.debug('El cliente ' + str(s.getsockname()) + ' recibió correctamente ' + str(bytes_recibidos) + ' bytes del archivo.')
        s.close()

reply = recv_all(socket_principal, 39).split(',')
num_bytes_SC = int(reply[0])
bytes_retransmitidos = int(reply[1])
num_paquetes_SC = int(reply[2])
paquetes_retransmitidos = int(reply[3])
if paquetes_retransmitidos == 0:
    log.info('El número de bytes recibidos fue: ' + str(num_bytes_SC) + ' bytes.')
    log.info('El número de paquetes recibidos fue: ' + str(num_paquetes_SC))
else:
    log.info('El número de bytes recibidos estuvo entre ' + str(num_bytes_SC - bytes_retransmitidos) + ' y ' + str(num_bytes_SC))
    log.info('El número de paquetes recibidos estuvo entre ' + str(num_paquetes_SC - paquetes_retransmitidos) + ' y ' + str(num_paquetes_SC))
socket_principal.close()

        