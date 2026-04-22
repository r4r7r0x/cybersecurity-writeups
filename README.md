
# 🔐 Cybersecurity Portfolio — r4r7r0x

> Penetration testing writeups and notes documenting my journey 
> into offensive security through HackTheBox and CTF platforms.

---

## 👤 About Me

I'm a 17-year-old cybersecurity enthusiast from Spain passionate 
about ethical hacking, penetration testing and red team operations.
Currently completing HackTheBox machines while building a strong 
foundation for a career in offensive security.

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

| # | Machine | OS | Difficulty | Techniques | Writeup |
|---|---------|-----|------------|------------|---------|
| 1 | Archetype | Windows | Easy | SMB Enumeration, MSSQL RCE, SeImpersonatePrivilege, winPEAS | [📄 Read](./HackTheBox/Archetype/writeup.md) |
| 2 | Oopsie | Linux | Easy | IDOR, Cookie Manipulation, File Upload, SUID PATH Hijacking | [📄 Read](./HackTheBox/Oopsie/writeup.md) |
| 3 | Vaccine | Linux | Easy | FTP Anonymous, ZIP Cracking, SQLi, sudo vi GTFOBins | [📄 Read](./HackTheBox/Vaccine/writeup.md) |
| 4 | UniFi | Linux | Easy | Log4Shell CVE-2021-44228, JNDI/LDAP, MongoDB Password Reset | [📄 Read](./HackTheBox/UniFi/writeup.md) |
| 5 | Included | Linux | Easy | LFI, TFTP Upload, LXD Container Escape | [📄 Read](./HackTheBox/Included/writeup.md) |
| 6 | Markup | Windows | Easy | XXE Injection, SSH Key Theft, Scheduled Task Abuse | [📄 Read](./HackTheBox/Markup/writeup.md) |
| 7 | Base | Linux | Easy | PHP Type Juggling, File Upload, sudo find GTFOBins | [📄 Read](./HackTheBox/Base/writeup.md) |

### Active Machines

| # | Machine | OS | Difficulty | Techniques | Writeup |
|---|---------|-----|------------|------------|---------|
| 8 | Lame | Linux | Easy | CVE-2007-2447, Samba RCE, Metasploit | [📄 Read](./HackTheBox/Lame/writeup.md) |
| 9 | Blue | Windows | Easy | MS17-010 EternalBlue, Metasploit, SMB | [📄 Read](./HackTheBox/Blue/writeup.md) |
| 10 | Legacy | Windows | Easy | MS08-067 CVE-2008-4250, MS17-010, Metasploit | [📄 Read](./HackTheBox/Legacy/writeup.md) |
| 11 | Devel | Windows | Easy | Anonymous FTP, ASPX Shell, MS10-015 KiTrap0D | [📄 Read](./HackTheBox/Devel/writeup.md) |
| 12 | Bashed | Linux | Easy | Webshell, sudo Escalation, Cronjob Abuse | [📄 Read](./HackTheBox/Bashed/writeup.md) |
| 13 | Shocker | Linux | Easy | Shellshock CVE-2014-6271, CGI Exploitation, sudo perl | [📄 Read](./HackTheBox/Shocker/writeup.md) |
| 14 | Knife | Linux | Easy | PHP 8.1.0-dev Backdoor, sudo knife GTFOBins | [📄 Read](./HackTheBox/Knife/writeup.md) |
| 15 | Nibbles | Linux | Easy | CVE-2015-6967, Nibbleblog File Upload, sudo Script Abuse | [📄 Read](./HackTheBox/Nibbles/writeup.md) |
| 16 | Grandpa | Windows | Easy | CVE-2017-7269, IIS 6.0 WebDAV, SeImpersonatePrivilege, churrasco | [📄 Read](./HackTheBox/Grandpa/writeup.md) |
| 17 | Granny | Windows | Easy | CVE-2017-7269, IIS 6.0 WebDAV, SeImpersonatePrivilege, churrasco | [📄 Read](./HackTheBox/Granny/writeup.md) |
| 18 | SolidState | Linux | Medium | Default Credentials, POP3 Enumeration, rbash Escape, Cronjob Abuse | [📄 Read](./HackTheBox/SolidState/writeup.md) |
| 19 | Bastard | Windows | Medium | CVE-2018-7600 Drupalgeddon2, SeImpersonatePrivilege, JuicyPotato | [📄 Read](./HackTheBox/Bastard/writeup.md) |

---

## 🛠️ Tools & Technologies

### Enumeration
- nmap, Gobuster, ffuf, wfuzz, smbclient, enum4linux, Nikto, Wappalyzer

### Exploitation
- Metasploit, Impacket, php-reverse-shell, Log4jUnifi, sqlmap, msfvenom, curl

### Web Security
- Burp Suite, Firefox DevTools

### Password Cracking
- John The Ripper, Hashcat, openssl, zip2john

### Privilege Escalation
- winPEAS, linPEAS, GTFOBins, LXD, SUID abuse, churrasco, JuicyPotato, local_exploit_suggester

### Post Exploitation
- netcat, telnet, psexec.py, mssqlclient.py, nc.exe, impacket-smbserver

### Databases
- MongoDB, PostgreSQL, MSSQL

### Protocols
- SMB, FTP, TFTP, SSH, LDAP, HTTP/HTTPS, WebDAV, SMTP, POP3

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
| Unrestricted File Upload | PHP shell upload and execution | Oopsie, Base, Devel |
| SUID PATH Hijacking | Fake binary via PATH manipulation | Oopsie |
| Anonymous FTP | Sensitive files exposed publicly | Vaccine, Devel |
| SQL Injection | Authenticated SQLi via sqlmap | Vaccine |
| Log4Shell CVE-2021-44228 | JNDI injection via login field | UniFi |
| MongoDB Abuse | Admin password reset via database | UniFi |
| Local File Inclusion | Reading system files via URL parameter | Included |
| TFTP Upload | Unauthenticated file upload | Included |
| LXD Privilege Escalation | Container escape to root | Included |
| XXE Injection | Reading system files via XML | Markup |
| SSH Key Theft | Private key extracted via XXE | Markup |
| PHP Type Juggling | strcmp() bypass via array input | Base |
| sudo Misconfiguration | find/vi/perl/knife/script allowed as root | Vaccine, Base, Shocker, Knife, Nibbles |
| CVE-2007-2447 | Samba username map script RCE | Lame |
| MS17-010 EternalBlue | SMBv1 remote code execution | Blue |
| MS08-067 CVE-2008-4250 | SMB remote code execution | Legacy |
| MS10-015 KiTrap0D | Windows kernel privilege escalation | Devel |
| FTP/Web Shared Root | Uploaded files executable via web | Devel |
| Exposed Webshell | phpbash accessible via hidden directory | Bashed |
| Cronjob Abuse | Writable script executed as root | Bashed, SolidState |
| Shellshock CVE-2014-6271 | RCE via bash CGI script | Shocker |
| PHP 8.1.0-dev Backdoor | RCE via User-Agentt zerodium header | Knife |
| CVE-2015-6967 | Nibbleblog authenticated file upload RCE | Nibbles |
| Default Credentials | Various default credentials accepted | Nibbles, SolidState |
| CVE-2017-7269 | IIS 6.0 WebDAV remote buffer overflow | Grandpa, Granny |
| SeImpersonatePrivilege | Token impersonation via churrasco/JuicyPotato | Grandpa, Granny, Bastard |
| Information Disclosure | SSH credentials in email / version in changelog | SolidState, Bastard |
| rbash Escape | Restricted shell bypass via script | SolidState |
| CVE-2018-7600 Drupalgeddon2 | Unauthenticated RCE in Drupal 7.54 | Bastard |

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

Pégalo en el README.md y haz commit con el mensaje Update README - Add Bastard. 🔥
