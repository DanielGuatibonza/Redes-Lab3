HOST = '127.0.0.1'
PORT = 8081

def recv_all (sock, length):
    data = ''
    while len(data) < length:
        more = (sock.recv(length - len(data))).decode()
        if not more:
            raise EOFError ('Socket cerrado.')
        data += more

    return data