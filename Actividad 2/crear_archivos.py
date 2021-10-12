tamano_archivo = input("Ingrese el tamaño del archivo que requiere (MB): ")
with open('ArchivosServidor/file' + tamano_archivo + '.txt', 'w') as nuevo_archivo:
    data = ''
    for _ in range(1024*1024*int(tamano_archivo)):
        data += 'a'
    nuevo_archivo.write(data)