- user.txt ✅
- root.txt ✅

---

## Tools Used

| Tool | Purpose |
|------|---------|
| nmap | Port and service enumeration |
| Burp Suite | Header analysis |
| searchsploit | Exploit research |
| CVE-2017-7269 exploit | Remote buffer overflow |
| impacket-smbserver | File transfer to target |
| churrasco.exe | SeImpersonatePrivilege abuse |
| netcat | Reverse shell listener |

---

## Vulnerabilities Found

| Vulnerability | Description |
|--------------|-------------|
| CVE-2017-7269 | IIS 6.0 WebDAV remote buffer overflow |
| SeImpersonatePrivilege | Token impersonation via churrasco |
