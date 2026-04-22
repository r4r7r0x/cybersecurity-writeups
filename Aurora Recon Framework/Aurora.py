#!/usr/bin/env python3

import argparse
import subprocess
import os
import json
import shutil
from datetime import datetime

# =========================
# COLORS
# =========================

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
GRAY = "\033[90m"

# =========================
# BANNER (PRO CLEAN)
# =========================

def banner():
    print(f"""
{CYAN}
╔══════════════════════════════════════╗
║        AURORA RECON FRAMEWORK        ║
║                                      ║
║     fast • modular • reliable        ║
╚══════════════════════════════════════╝
{RESET}
              by r4r7r0x
""")

# =========================
# UTILS
# =========================

def run(cmd):
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return p.stdout
    except:
        return ""

def mkdir(path):
    os.makedirs(path, exist_ok=True)

def tool_exists(name):
    return shutil.which(name) is not None

# =========================
# WORKSPACE
# =========================

def workspace(target):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"aurora_{target}_{ts}"
    mkdir(path)
    return path

# =========================
# SCAN ENGINE
# =========================

def nmap_scan(target):
    cmd = f"nmap -Pn -T4 -sC -sV --open {target}"
    return run(cmd)

# =========================
# PARSER
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

        except (ValueError, IndexError):
            continue

    return services

# =========================
# MODULES
# =========================

def http_enum(target, port):
    url = f"http://{target}:{port}"

    if not tool_exists("gobuster"):
        return {"url": url, "error": "gobuster not installed"}

    cmd = f"gobuster dir -u {url} -w /usr/share/wordlists/dirb/common.txt -q"
    out = run(cmd)

    return {
        "url": url,
        "paths": [l.strip() for l in out.splitlines() if l.strip()]
    }

def smb_enum(target):
    return {"note": "Use smbclient / enum4linux manually for deeper enumeration"}

def ssh_enum(target, port):
    return {"banner": run(f"nc -w3 {target} {port}")}

# =========================
# SUMMARY (PRO OUTPUT)
# =========================

def summary(services):
    print(f"\n{BOLD}{CYAN}──────── SUMMARY ────────{RESET}")

    if not services:
        print(f"{RED}No open services found{RESET}")
        return

    for s in services:
        port = s["port"]
        svc = s["service"]

        tag = "OTHER"

        if port == 80 or port == 443:
            tag = "HTTP"
        elif port == 22:
            tag = "SSH"
        elif port == 445:
            tag = "SMB"

        print(f"{GREEN}[+] {port:<5}{RESET} → {svc:<10} [{tag}]")

    print(f"{CYAN}─────────────────────────{RESET}\n")

# =========================
# REPORT
# =========================

def generate_report(target, services, findings, notes, outdir):
    data = {
        "target": target,
        "services": services,
        "findings": findings,
        "notes": notes or []
    }

    with open(f"{outdir}/report.json", "w") as f:
        json.dump(data, f, indent=4)

# =========================
# MAIN
# =========================

def main():
    parser = argparse.ArgumentParser(description="Aurora Recon Framework")

    parser.add_argument("-t", "--target", required=True)
    parser.add_argument("--htb", action="store_true")
    parser.add_argument("--notes", action="append")

    args = parser.parse_args()

    banner()

    outdir = workspace(args.target)

    print(f"{GRAY}[*] Running scan on {args.target}...{RESET}")

    nmap_out = nmap_scan(args.target)

    with open(f"{outdir}/nmap.txt", "w") as f:
        f.write(nmap_out)

    services = parse_nmap(nmap_out)

    findings = {}

    for s in services:
        if s["port"] == 80:
            findings["http"] = http_enum(args.target, 80)

        elif s["port"] == 445:
            findings["smb"] = smb_enum(args.target)

        elif s["port"] == 22:
            findings["ssh"] = ssh_enum(args.target, 22)

    generate_report(args.target, services, findings, args.notes, outdir)

    summary(services)

    print(f"{GREEN}[+] Done → {outdir}{RESET}")

if __name__ == "__main__":
    main()