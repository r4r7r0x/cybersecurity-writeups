# 🔐 Cybersecurity Portfolio — r4r7r0x

> Penetration testing writeups and notes documenting my journey 
> into offensive security through HackTheBox and CTF platforms.

---

## 👤 About Me

I'm a 17-year-old cybersecurity enthusiast from Spain passionate 
about ethical hacking, penetration testing and red team operations.
Currently completing HackTheBox Starting Point machines while 
building a strong foundation for a career in offensive security.

**Goals:**
- eJPT certification — July 2026
- CompTIA Security+ — 2026/2027
- OSCP — 2028

**Focus areas:**
- Penetration Testing
- Red Team Operations
- Web Application Security
- Privilege Escalation

---

## 📚 HackTheBox Writeups

### Starting Point — Tier 2 (Complete ✅)

| Machine | OS | Difficulty | Techniques | Status |
|---------|----|------------|------------|--------|
| [Archetype](./HackTheBox/Archetype/writeup.md) | Windows | Easy | SMB Enumeration, MSSQL RCE, SeImpersonatePrivilege, winPEAS | ✅ |
| [Oopsie](./HackTheBox/Oopsie/writeup.md) | Linux | Easy | IDOR, Cookie Manipulation, File Upload, SUID PATH Hijacking | ✅ |
| [Vaccine](./HackTheBox/Vaccine/writeup.md) | Linux | Easy | FTP Anonymous, ZIP Cracking, SQLi, sudo vi GTFOBins | ✅ |
| [UniFi](./HackTheBox/UniFi/writeup.md) | Linux | Easy | Log4Shell CVE-2021-44228, JNDI/LDAP, MongoDB Password Reset | ✅ |
| [Included](./HackTheBox/Included/writeup.md) | Linux | Easy | LFI, TFTP Upload, LXD Container Escape | ✅ |
| [Markup](./HackTheBox/Markup/writeup.md) | Windows | Easy | XXE Injection, SSH Key Theft, Scheduled Task Abuse | ✅ |
| [Base](./HackTheBox/Base/writeup.md) | Linux | Easy | PHP Type Juggling, File Upload, sudo find GTFOBins | ✅ |

---

## 🛠️ Tools & Technologies

### Enumeration
- nmap, Gobuster, ffuf, smbclient, enum4linux

### Exploitation
- Metasploit, Impacket, php-reverse-shell, Log4jUnifi, sqlmap

### Web Security
- Burp Suite, Firefox DevTools

### Password Cracking
- John The Ripper, Hashcat, openssl, zip2john

### Privilege Escalation
- winPEAS, linPEAS, GTFOBins, LXD, SUID abuse

### Post Exploitation
- netcat, psexec.py, mssqlclient.py, nc.exe

### Databases
- MongoDB, PostgreSQL, MSSQL

### Protocols
- SMB, FTP, TFTP, SSH, LDAP, HTTP/HTTPS

### Scripting
- Python, Bash, PowerShell

---

## 🎯 Vulnerabilities Exploited

| Vulnerability | Description | Machine |
|--------------|-------------|---------|
| SMB Enumeration | Sensitive files exposed on SMB share | Archetype |
| MSSQL xp_cmdshell | OS command execution via SQL Server | Archetype |
| IDOR | User enumeration via URL parameter | Oopsie |
| Broken Access Control | Cookie manipulation for admin access | Oopsie |
| Unrestricted File Upload | PHP shell upload and execution | Oopsie, Base |
| SUID PATH Hijacking | Fake binary via PATH manipulation | Oopsie |
| Anonymous FTP | Sensitive backup exposed publicly | Vaccine |
| SQL Injection | Authenticated SQLi via sqlmap | Vaccine |
| Log4Shell CVE-2021-44228 | JNDI injection via login field | UniFi |
| MongoDB Abuse | Admin password reset via database | UniFi |
| Local File Inclusion | Reading system files via URL parameter | Included |
| TFTP Upload | Unauthenticated file upload | Included |
| LXD Privilege Escalation | Container escape to root | Included |
| XXE Injection | Reading system files via XML | Markup |
| SSH Key Theft | Private key extracted via XXE | Markup |
| PHP Type Juggling | strcmp() bypass via array input | Base |
| sudo Misconfiguration | find/vi allowed as root via sudo | Vaccine, Base |

---

## 📜 Certifications Roadmap
2026  ──────────────────────────────────────────────────────────
[July] eJPT
[Sept] Start SMR (Sistemas Microinformáticos y Redes)
[Dec]  CompTIA Security+
2027  ──────────────────────────────────────────────────────────
Start ASIR (Administración de Sistemas Informáticos)
2028  ──────────────────────────────────────────────────────────
OSCP

---

## ⚠️ Disclaimer

All writeups are based on legal lab environments such as HackTheBox.
This content is strictly for educational purposes.
Never attempt these techniques on systems without explicit permission.
