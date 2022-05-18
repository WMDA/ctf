import subprocess
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
    print(scapy_packet.show())
    packet.accept()


try:
    options=get_arguments()
    if options.test:
        subprocess.call(["iptables","-I","OUTPUT","-j","NFQUEUE","--queue-num","0"])
        subprocess.call(["iptables","-I","INPUT","-j","NFQUEUE","--queue-num","0"])
    else:
        subprocess.call(["iptables","-I","Forward","-j","NFQUEUE","--queue-num","0"])
    queue = nfq.NetfilterQueue()
    queue.bind(0, packet_processor)
    queue.run()
except KeyboardInterrupt:
    print('\nUser requested termination...flusing IP tables')
    subprocess.call(["iptables","--flush",])
    sys.exit()
