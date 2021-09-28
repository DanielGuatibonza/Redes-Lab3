import pyshark

capture = pyshark.LiveCapture(interface='ens33')
capture.sniff(timeout=50)

contador = 0
for packet in capture:
    #print('Just arrived:', packet)
    contador += 1
    print(contador)
