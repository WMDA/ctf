#!/usr/bin/env python3

import scapy.all as scapy
import argparse
from datetime import datetime
import sys

def ip():
    parse = argparse.ArgumentParser()
    parse.add_argument("-ip", dest="ip", help="Needs IP range /24")
    parse.add_argument("-i", dest="interface", help='Needs interface')
    parse.add_argument("-t", dest="time", help="Number of packets sent")
    options= parse.parse_args()
    if not options.ip:
        parse.error('>> Needs ip address. Use -h for further details.')
    elif not options.interface:
        parse.error('>> Needs interface. Use -h for further details')
    else:
        return options


def scan(ip,interface,timer=5):
    client_list=[]
    while timer >0:
        arp_request = scapy.ARP(pdst = ip)
        broadcast= scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        ans = scapy.srp(arp_request_broadcast, timeout=1,iface=interface, verbose=False)[0]
        for i in ans:
            client_dic={'IP':i[1].psrc, 'MAC':i[1].hwsrc}
            if client_dic not in client_list:
                client_list.append(client_dic)
        timer = timer -1
    return client_list

def output(results_list):
    print('','-'*100,'\n',"\t IP \t\t\tMac address",'\n','-'*100)
    for i in results_list:
        print('\t',i['IP'] + "\t\t" + i['MAC'])

options = ip()
print('\nScanning please wait:\n ')
start=datetime.now()
try:
    if options.time:
        scan_results=scan(options.ip, options.interface,int(options.time))
    else:
        scan_results=scan(options.ip, options.interface)
    output(scan_results)
except KeyboardInterrupt:
    print('User requested shut down:')
    sys.exit()
stop=datetime.now()
duration= stop-start
print('-'*100,'\nScan Complete\n')
print('Scan duration: %s'%(duration))
