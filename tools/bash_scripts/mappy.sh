#!/bin/bash

function usage {
	echo -e '\nScript to automate my nmap enumeration. 
	          Runs a -sC -sV on top ports.\n Then does an all ports scan using -sC -sV. 
	          \n Does a -A --script=vuln scan. 
	          Finall will offer to do a UDP scan of top 20 ports.
	          Saves output to a enum/nmap directory. Can skip the all port/aggressive/UDP scan nmap scan \n\nUSAGE:'
	echo -e '\t-i:\ip address.'
	exit 0
}

argparse=i:h

while getopts ${argparse} options

do
	case "${options}" in

	i) ip=${OPTARG};;

    h) usage
    
    esac
done

if [ -z $ip ];
then
	echo -e "\n\e[31mplease provide ip address\e[0m"
	exit 1
else
	echo -e "Scanning" ${ip}
fi

nmap -sC -sV -oN enum/nmap/initial -vv ${ip}

echo -e "\n\e[33mFinished with first scan. Would you like me to continue with an all port scan? (y/n)\e[0m"

read response

if [[ $response == "y" ]];
then
	echo -e "\n\e[33mStarting all ports scan\n\e[0m"
	nmap -sC -sV -p- -oN enum/nmap/all_ports -vv ${ip}
    
else
	echo -e "\n\e[31mCancelling all ports scan\e[0m"
	fi

echo -e "\n\e[33mWould you like me to continue with the vuln scan? (y/n)\e[0m"

read aggressive_response

if [[ $aggressive_response == 'y' ]];
then
	nmap -A --script=vuln -oN enum/nmap/aggressive -vv ${ip}

else
	echo -e "\n\e[31mCancelling aggressive scan\e[0m"
	fi 

echo -e "\e[33m\nWould you like me to enumerate top 20 UDP ports? (y/n)\e[0m"
read udp_response

if [[ $udp_response == 'y' ]];
then
	nmap -sU -oN enum/nmap/udp --top-ports=20 -vv ${ip}

else
	echo -e "\n\e[31mCancelling UDP scan\e[0m"
	fi 





