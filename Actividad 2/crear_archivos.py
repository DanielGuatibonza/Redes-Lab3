from settings import *
tamano_archivo = input("Ingrese el tamaño del archivo que requiere (MB): ")
with open('ArchivosServidor/file' + tamano_archivo + '.txt', 'w') as nuevo_archivo:
    data = ''
    ord_letra = 97
    for i in range(1024*1024*int(tamano_archivo) // CHUNKS_SIZE):
        if ord_letra == 123:
            ord_letra = 97
        letra = chr(ord_letra)
        data += letra*(CHUNKS_SIZE - 1) + '\n'
        ord_letra += 1
    nuevo_archivo.write(data)
