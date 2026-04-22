#!/usr/bin/env python3

import argparse
import subprocess
import os
import json
import shutil
from datetime import datetime

# =========================
# CONFIG
# =========================

DEFAULT_WORDLIST = "/usr/share/wordlists/dirb/common.txt"

# =========================
# BANNER (FIXED + CLEAN)
# =========================

def banner():
    print(r"""
 █████╗ ██╗   ██╗██████╗  ██████╗ ██████╗  █████╗
██╔══██╗██║   ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗
███████║██║   ██║██████╔╝██║   ██║██████╔╝███████║
██╔══██║██║   ██║██╔══██╗██║   ██║██╔══██╗██╔══██║
██║  ██║╚██████╔╝██║  ██║╚██████╔╝██║  ██║██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═╝  ╚═╝

        Aurora Recon Framework
              by r4r7r0x
""")

# =========================
# UTILS
# =========================

def run(cmd):
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return p.stdout
    except Exception as e:
        return str(e)

def mkdir(path):
    os.makedirs(path, exist_ok=True)

def tool_exists(t):
    return shutil.which(t) is not None

# =========================
# WORKSPACE
# =========================

def workspace(target):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"aurora_{target}_{ts}"
    mkdir(path)
    return path

# =========================
# SCAN
# =========================

def nmap_scan(target):
    # FIX REAL: -Pn evita false negatives (MUY IMPORTANTE EN HTB)
    cmd = f"nmap -Pn -T4 -sC -sV --open {target}"
    return run(cmd)

# =========================
# PARSER (ROBUSTO)
# =========================

def parse_nmap(output):
    services = []

    for line in output.splitlines():
        if "/tcp" not in line or "open" not in line:
            continue

        parts = line.split()

        try:
            port = int(parts[0].split("/")[0])
            service = parts[2]
            version = " ".join(parts[3:]) if len(parts) > 3 else ""

            services.append({
                "port": port,
                "service": service,
                "version": version
            })

        except (IndexError, ValueError):
            continue

    return services

# =========================
# MODULES (BASIC BUT RELIABLE)
# =========================

def http_enum(target, port, outdir, wordlist):
    url = f"http://{target}:{port}"

    if not tool_exists("gobuster"):
        return {"url": url, "error": "gobuster not installed"}

    cmd = f"gobuster dir -u {url} -w {wordlist} -q --no-error"
    out = run(cmd)

    return {
        "url": url,
        "paths": [l for l in out.splitlines() if l.strip()]
    }

def smb_enum(target):
    if not tool_exists("smbclient"):
        return {"error": "smbclient not installed"}

    return {"note": "manual enum recommended (smbclient / enum4linux)"}

def ssh_enum(target, port):
    return {"banner": run(f"nc -w3 {target} {port}")}

# =========================
# MAIN
# =========================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", required=True)
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--htb", action="store_true")
    parser.add_argument("--notes", action="append")

    args = parser.parse_args()

    banner()

    wordlist = DEFAULT_WORDLIST
    if args.htb:
        wordlist = "/usr/share/seclists/Discovery/Web-Content/common.txt"

    outdir = workspace(args.target)

    print("[*] Running nmap...")
    nmap_out = nmap_scan(args.target)

    with open(f"{outdir}/nmap.txt", "w") as f:
        f.write(nmap_out)

    services = parse_nmap(nmap_out)

    if not services:
        print("[-] No open ports found")
        return

    findings = {}

    for s in services:
        port = s["port"]

        if port == 80 or port == 443:
            findings[f"http_{port}"] = http_enum(args.target, port, outdir, wordlist)

        elif port == 445:
            findings["smb"] = smb_enum(args.target)

        elif port == 22:
            findings["ssh"] = ssh_enum(args.target, port)

    report = {
        "target": args.target,
        "services": services,
        "findings": findings,
        "notes": args.notes or []
    }

    with open(f"{outdir}/report.json", "w") as f:
        json.dump(report, f, indent=4)

    print(f"[+] Done → {outdir}")

if __name__ == "__main__":
    main()