#!/usr/bin/env python3

import subprocess
import argparse
import random
import re


# Generates a random mac address based on pythons hexidecimal system and random library
def mac_generator():
    mac_address = "02:%02x:%02x:%02x:%02x:%02x" % (random.randint(0, 255),random.randint(0, 255),
    random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    return(mac_address)

# Generates command line interface options for interface, user specified mac address and random mac address
def get_arguments():
    parse = argparse.ArgumentParser()
    parse.add_argument("-i", "--interface", dest='interface', required=True, help='Interface to change mac address.')
    parse.add_argument("-m","--mac", dest='mac',help='New mac address, can use -r to generate random.')
    parse.add_argument("-r", help='Randomly assigns mac address.', action='store_true')
    options= parse.parse_args()
    if options.r:
        options.mac = mac_generator()
    if not options.mac:
        parse.error(">> Needs mac address. Use -m or -r. Use -h for more information.")
    else:
        return options

# Changes mac address using subprocess library
def change_mac (interface, mac):
    print (">> changing: " + interface + " to " + mac )
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw","ether", mac])
    subprocess.call(["ifconfig", interface, "up"])

# Returns output of changer
def mac_checker(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface]).decode('utf-8')
    search_result= re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if search_result:
        return(search_result.group(0))


options = get_arguments()
os.system(options.interface, + '')
change_mac(options.interface, options.mac)
mac_value= mac_checker(options.interface)

# Returns error if user specified mac address or random mac address doesn't match up to output
if not mac_value == options.mac:
    print('error in mac address')
