# 🔐 Cybersecurity Portfolio

Personal collection of CTF writeups and penetration testing notes.
Documenting my learning journey through platforms like HackTheBox.

---

## About Me

Cybersecurity enthusiast focused on penetration testing and ethical hacking.
Currently practicing on HackTheBox and building hands-on skills in:

- Network enumeration
- Web application security
- Windows/Linux privilege escalation
- SQL injection and database attacks
- CVE exploitation
- Container security
- File inclusion vulnerabilities
- XML injection attacks
- Password cracking

---

## HackTheBox Writeups

| Machine | OS | Difficulty | Status |
|---------|----|------------|--------|
| [Archetype](./HackTheBox/Archetype/writeup.md) | Windows | Easy | ✅ |
| [Oopsie](./HackTheBox/Oopsie/writeup.md) | Linux | Easy | ✅ |
| [Vaccine](./HackTheBox/Vaccine/writeup.md) | Linux | Easy | ✅ |
| [UniFi](./HackTheBox/UniFi/writeup.md) | Linux | Easy | ✅ |
| [Included](./HackTheBox/Included/writeup.md) | Linux | Easy | ✅ |
| [Markup](./HackTheBox/Markup/writeup.md) | Windows | Easy | ✅ |

---

## Tools & Technologies

- **Enumeration:** nmap, smbclient, Gobuster, enum4linux
- **Exploitation:** Metasploit, Impacket, php-reverse-shell, Log4jUnifi
- **Web:** Burp Suite, Firefox DevTools, sqlmap
- **Password Cracking:** John The Ripper, Hashcat, openssl
- **Privilege Escalation:** winPEAS, linPEAS, strings, find, GTFOBins, LXD
- **Post Exploitation:** netcat, psexec.py, mssqlclient.py, nc.exe
- **Databases:** MongoDB, PostgreSQL, MSSQL
- **Protocols:** SMB, FTP, TFTP, SSH, LDAP
- **Scripting:** Python, Bash, PowerShell
- **OS:** Parrot OS, Kali Linux, Windows

---

## Vulnerabilities Exploited

| Vulnerability | Machine |
|--------------|---------|
| SMB Enumeration + MSSQL RCE | Archetype |
| IDOR + Broken Access Control + File Upload | Oopsie |
| FTP Anonymous + ZIP Cracking + SQLi | Vaccine |
| Log4Shell CVE-2021-44228 | UniFi |
| LFI + TFTP Upload | Included |
| XXE Injection + SSH Key Theft | Markup |

---

## Certifications (Planned)

- eJPT — July 2026
- CompTIA Security+ — During SMR
- OSCP — During ASIR

---

## Disclaimer

All writeups are based on legal lab environments (HackTheBox, TryHackMe).
This content is for educational purposes only.
