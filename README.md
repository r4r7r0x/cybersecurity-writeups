
# r4r7r0x | Offensive Security Portfolio

Cybersecurity student focused on penetration testing, network exploitation, and offensive security tooling.

-----

## 🧠 Profile Summary

I focus on understanding systems from an attacker’s perspective, combining manual exploitation techniques with automation to improve reconnaissance and attack efficiency.

Main interests:

- Network exploitation (ARP, MITM, LAN attacks)
- Web application security
- Privilege escalation (Linux & Windows)
- Security tool development and automation

-----

## 🧰 Technical Skills

### Operating Systems

- Parrot OS
- Kali Linux

### Reconnaissance & Enumeration

- Nmap
- Gobuster
- Netcat

### Exploitation

- SQL Injection
- LFI / RFI
- Remote Code Execution (RCE)
- Service misconfigurations

### Privilege Escalation

- Linux: SUID, sudo rules, cron jobs, capabilities
- Windows: services, weak permissions, token abuse

### Scripting & Tools

- Python (security automation)
- Bash (basic tooling & automation)

-----

## 🛠️ Projects

### Aurora Recon Framework

Automated reconnaissance framework for penetration testing and CTF environments.

Structures initial enumeration into a repeatable, fast and modular workflow, producing both raw tool outputs and a structured JSON report for analysis.

Key features:

- Network scanning via Nmap (fast / default / full modes)
- Service identification and automatic module dispatch (HTTP, SMB, SSH, MySQL)
- HTB mode with optimized wordlists and timeouts
- Isolated workspace per target with full output preservation
- Loot system for analyst notes, credentials, and interesting findings

```bash
python3 aurora.py -t <IP> [--fast|--full] [--htb] [--silent] [--notes "..."]
```

> Authorized use only — developed for use in controlled lab environments.

-----

### ARP Spoofing Tool

Custom tool implementing ARP spoofing techniques for understanding LAN-level attacks and MITM scenarios.

Key objectives:

- Understand ARP protocol behavior
- Simulate traffic interception in local networks
- Study packet redirection mechanisms

-----

## 📁 Hack The Box Writeups

Structured collection of machines solved on Hack The Box, focused on learning exploitation paths and privilege escalation techniques.

-----

## 🟢 Easy Machines

Focus: fundamentals of enumeration and basic exploitation.

|Machine  |Key Techniques                         |
|---------|---------------------------------------|
|Lame     |Samba CVE-2007-2447, Metasploit        |
|Legacy   |MS08-067, Windows SMB exploitation     |
|Blue     |MS17-010 (EternalBlue)                 |
|Devel    |FTP + IIS misconfiguration, token abuse|
|Grandpa  |WebDAV RCE, token impersonation        |
|Granny   |WebDAV misconfiguration                |
|Bashed   |Web-based shell, sudo abuse            |
|Shocker  |Shellshock (CVE-2014-6271)             |
|Knife    |PHP backdoor RCE                       |
|Archetype|MSSQL misconfiguration, Windows privesc|
|Oopsie   |IDOR, SUID privilege escalation        |
|Vaccine  |SQL injection, sudo misconfiguration   |
|Unifi    |Log4Shell (CVE-2021-44228), MongoDB    |
|Include  |LFI, privilege escalation              |
|Nibbles  |Nibbleblog RCE, sudo abuse             |
|Markup   |XXE injection, scheduled task abuse    |

-----

## 🟡 Medium Machines

Focus: chaining vulnerabilities and deeper service exploitation.

|Machine   |Key Techniques                         |
|----------|---------------------------------------|
|SolidState|Restricted shell escape, cron job abuse|
|Bastard   |Drupal RCE, token impersonation        |

-----

## 🧠 Methodology

My standard penetration testing workflow:

1. Reconnaissance — open ports and service fingerprinting
1. Enumeration — service-specific analysis and attack surface mapping
1. Exploitation — manual first, automation as support
1. Privilege Escalation — systematic local enumeration
1. Documentation — clean notes and reproducible steps

-----

## 📈 Current Focus

- Building offensive security tools beyond writeups
- Automating reconnaissance workflows
- Improving vulnerability chaining understanding
- Advancing toward eJPT (target: July 2026) and OSCP-level methodology

-----

## ⚠️ Disclaimer

All activities and tools are developed strictly for educational purposes in controlled environments such as Hack The Box and similar platforms.