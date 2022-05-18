#!/bin/bash

#Script to prepare Kali machine, after fresh install 
#Assumes running as root (I know I shouldn't but old habits)

#Update System.

apt-get update
apt-get upgrade -y
apt-get distro-upgrade -y

#Install programmes I like

apt-get install terminator -y
apt-get install gobuster -y
apt-get install bat -y

#Set up python.
apt-get install python3-pip -y
apt-get install python3-dev -y

#Install go for metasploit 
apt install -y golang

#Get sublime
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | apt-key add -
apt-get install apt-transport-https
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
apt-get update
apt-get install sublime-text -y

#Write to .zshrc
cd
echo "export GOROOT=/usr/lib/go" >> .zshrc
echo "export GOPATH=$HOME/go" >> .zshrc
echo "export PATH=$GOPATH/bin:$GOROOT/bin:$PATH" >> .zshrc

echo "alias python=python3" >>.zshrc
echo "alias pip=pip3" >>.zshrc

#Get git repos
cd /opt
git clone https://github.com/carlospolop/PEASS-ng.git
git clone https://github.com/AonCyberLabs/Windows-Exploit-Suggester.git
wget https://github.com/PowerShellMafia/PowerSploit/tree/master/Privesc

#Config file structure
cd ~
mkdir hacking 
mkdir hacking/thm hacking/htb hacking/vulnhub
mkdir tools
mkdir tools/linux_privesc tools/win_privesc

# Python packages
pip install pwncat-cs
pip install python-wappalyzer
