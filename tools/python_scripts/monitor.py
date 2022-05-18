#!/usr/bin/env python3

import subprocess

subprocess.call("ifconfig wlan0 down", shell=True)
subprocess.call("iwconfig wlan0 mode monitor", shell=True)
subprocess.call("ifconfig wlan0 up", shell=True)
