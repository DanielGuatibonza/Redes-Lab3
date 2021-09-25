import socket
HOST = '192.168.231.132'
PORT = 8081

CLIENTE_ACEPTADO = 'Su conexión fue exitosa.'
CLIENTE_LISTO = 'Actualmente me encuentro activo para recibir archivos'
ARCHIVO_RECIBIDO = 'El archivo se recibió correctamente.              '
HASH_INCORRECTO = 'La integridad del archivo s ha visto comprometida.'

def recv_all(sock, length):
    data = ''
    while len(data) < length:
        packet = sock.recv(length - len(data), socket.MSG_TRUNC)
        print(len(packet))
        more = packet.decode()
        if not more:
            raise EOFError ('Socket cerrado.')
        data += more
    return data