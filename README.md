# Redes-Lab3
## Instrucciones de instalación
Para instalar los aplicativos de cliente y servidor, únicamente se requiere clonar/descargar este repositorio en las máquinas donde se ejecutará el servicio respectivo. Es necesario contar con el repositorio completo ya que este cuenta con la estructura de carpetas que los archivos principales de cada aplicativo requieren para su correcta ejecución. Cabe aclarar que la instalación del servidor debe realizarse en una máquina Ubuntu ya que en esta se requiere instalar adicionalmente *tshark*. Para lo anterior basta con ejecutar los siguientes comandos:

    > sudo apt-get update -y
    > sudo apt-get install -y tshark
    
## Ejecución de los programas
El repositorio cuenta con dos implementaciones para la transferencia de archivos: TCP (Actividad 1) y UDP (Actividad 2). De acuerdo a la implementación que se desee probar, es decir, dentro de la carpeta respectiva, es necesario editar los parámetros de configuración para la conexión entre ambos equipos previo a la ejecución de cualquiera de los servicios. De esta forma, se deben editar, tanto en el cliente como en el servidor, las constantes HOST y CLIENT_HOST el archivo *settings.py* para que estas correspondan con las direcciones IP del equipo servidor y cliente respectivamente.

### Servidor
Antes de poder ejecutar el aplicativo del servidor, en la carpeta "ArchivosServidor" se deben encontrar los archivos que se desean transmitir. Estos archivos deben estar nombrados de la forma *file<numMB>.txt* donde *<numMB>* corresponde al número de mega-bytes del archivo. Para generar estos archivos se desarrolló el programa *crear_archivos.py* que se encarga de crear el archivo de texto dentro de esta carpeta del tamaño que se le especifique a la hora de su ejecución. Considerando que este programa fue desarrollado también en Python, basta con ejecutar el siguiente comando para utilizarlo.

    > python3 crear_archivo.py
  
Una vez creados los archivos a transmitir, la ejecución del servidor se realiza nuevamente con Python esta vez otorgandole permisos de super usuario.
  
    > sudo python3 server.py  

Al ejecutar el servidor, este solicitará el tamaño del archivo que se desea transmitir y el número de clientes de los que espera conexión para efectuar la transmisión de forma simultánea.
  
### Cliente
En el lado del cliente no se debe realizar ninguna configuración previa por lo que, luego de ejecutar el servicio del servidor, basta con ejecutar el archivo del cliente:
  
    > sudo python3 server.py  
  
Después de haberse realizado la transferencia, en la máquina cliente se tendrán los archivos recibidos en la carpeta "ArchivosRecibidos" y en la carpeta "Logs" se encontrarán los archivos *log* tanto del cliente como del servidor con la información sobre la transferencia y ciertas estadísticas asociadas a la misma. Cabe resaltar sobre estas estadísiticas que del lado del cliente se presenta un rango tanto de paquetes como de bytes recibidos ya que el margen entre ambos límites corresponde a los datos que fueron retransmitidos por parte del servidor.
  
## Video de explicación del desarrollo
[Redes - Laboratorio 3 - Desarrollo](https://www.youtube.com/watch?v=PK61OhJ0aM0)
  
## Video de funcionamiento
[Redes - Laboratorio 3 - Funcionamiento](https://www.youtube.com/watch?v=QGB3ZIjFj3Q)
