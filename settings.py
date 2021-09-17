PORT = 8000

def recv_all (sock, length):
    data = ''
    while len(data) < length:
        more = sock.recv (length - len(data))

        if not more:
            raise EOFError ('Socket closed %d bytes into a %d-byte message')

        data += more

    return data