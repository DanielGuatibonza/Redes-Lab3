import pyshark

capture = pyshark.LiveCapture(interface='ens33')
capture.sniff(timeout=30)
print(len(capture))
print(dir(capture[0]))
for packet in capture:
     print(packet.captured_length())
#     contador += 1
#     print(contador)
