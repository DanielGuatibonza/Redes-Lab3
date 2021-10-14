import socket
import sys
from settings import *
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import hashlib
import logging
import time

formated_date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
logging.basicConfig(filename='Logs/Cliente/'+formated_date + '-log.log',
                    filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger('Logs/Cliente/'+formated_date + '-log')
log.setLevel(logging.DEBUG)

socket_principal = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_principal.sendto(SOLICITAR_CONEXION.encode(), (HOST, PORT))
data, server_address = socket_principal.recvfrom(CHUNKS_SIZE)
data = data.decode()

num_clientes = int(data.split(',')[0])
file_size_MB = data.split(',')[1]
file_size = 1024*1024*int(file_size_MB)
log.debug('Archivo a recibir: file' + file_size_MB +
          '.txt, Tamaño: ' + file_size_MB + 'MB.')


def recibir_archivo(i):
    global file_size, num_clientes, server_address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    identificador = str(i) if i >= 10 else '0'+str(i)
    s.sendto((CLIENTE_LISTO+':'+identificador).encode(), server_address)
    reply, server_address = s.recvfrom(CHUNKS_SIZE)
    print('El servidor respondió con: ', str(reply.decode()))
    start_time = time.time()

    file_data = ""
    file_chunk = ""
    while(True):
        file_chunk, server_address = s.recvfrom(CHUNKS_SIZE)
        if (len(file_chunk) != 64):
            file_data += file_chunk.decode()
        else:
            break

    log.debug('El tiempo de transferencia del archivo al cliente ' +
              str(s.getsockname()) + ' fue de ' + str(time.time() - start_time) + ' segundos.')
    hash_data = hashlib.sha256(file_data.encode()).hexdigest()
    hash_server = file_chunk
    if len(file_data) == file_size and hash_data == hash_server:
        with open('ArchivosRecibidos/Cliente{}-Prueba-{}.txt'.format(i, num_clientes), 'w') as archivo:
            archivo.write(file_data)
        print(identificador)
        s.sendto((ARCHIVO_RECIBIDO+':'+identificador).encode(), server_address)
    else:
        print(identificador)
        s.sendto((ARCHIVO_INCORRECTO+':'+identificador).encode(), server_address)
    return s, len(file_data)


with ThreadPoolExecutor(max_workers=25) as pool:
    futures = {pool.submit(recibir_archivo, i+1) for i in range(num_clientes)}
    for fut in as_completed(futures):
        s, bytes_recibidos = fut.result()
        print(
            f"El tamaño del archivo recibido fue de {bytes_recibidos} bytes.")
        log.debug('El cliente ' + str(s.getsockname()) +
                  ' recibió correctamente ' + str(bytes_recibidos) + ' bytes del archivo.')
        s.close()

# reply, server_address = socket_principal.recvfrom(CHUNKS_SIZE)
# reply = reply.decode().split(',')
# num_bytes_CS = int(reply[0])
# num_paquetes_CS = int(reply[1])

# log.info('El número de bytes recibidos es de ' + str(num_bytes_CS))
# log.info('El número de paquetes recibidos es de ' + str(num_paquetes_CS))
socket_principal.close()
