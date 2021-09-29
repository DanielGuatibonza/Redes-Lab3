import pyshark

cap = pyshark.FileCapture(input_file='traff.pcap')

print(cap)
print(len(cap))
print(dir(cap))

cap.close()

# import scapy.all as scapy

# cap = scapy.rdpcap('traff.pcap')

# print(scapy.sniff(offline="traff.pcap", filter="tcp.analysis.retransmission"))