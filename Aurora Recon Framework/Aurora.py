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
GREEN = "\033[92m"
CYAN = "\033[96m"
RED = "\033[91m"
GRAY = "\033[90m"
BOLD = "\033[1m"

# =========================
# BANNER (CLEAN + PRO)
# =========================

def banner():
    print(f"""
{CYAN}
╔══════════════════════════════════════╗
║        AURORA RECON FRAMEWORK        ║
║                                      ║
║     fast • clean • modular • HTB     ║
╚══════════════════════════════════════╝
{RESET}
              by r4r7r0x
""")

# =========================
# UTILS
# =========================

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
    except:
        return ""

def mkdir(path):
    os.makedirs(path, exist_ok=True)

def tool_exists(t):
    return shutil.which(t) is not None

# =========================
# WORKSPACE (FIXED: ABSOLUTE PATH SAFE)
# =========================

def create_workspace(target, base_dir):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = target.replace("/", "_").replace(":", "_")

    full_path = os.path.join(os.path.abspath(base_dir), f"aurora_{safe}_{ts}")
    mkdir(full_path)

    return full_path

# =========================
# NMAP SCAN
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

        except:
            continue

    return services

# =========================
# MODULES
# =========================

def http_enum(target, port):
    if not tool_exists("gobuster"):
        return {"error": "gobuster not installed"}

    url = f"http://{target}:{port}"
    cmd = f"gobuster dir -u {url} -w /usr/share/wordlists/dirb/common.txt -q"

    out = run(cmd)

    return {
        "url": url,
        "paths": [l.strip() for l in out.splitlines() if l.strip()]
    }

def ssh_enum(target, port):
    return {"banner": run(f"nc -w3 {target} {port}")}

def smb_enum(target):
    return {"note": "Use enum4linux or smbclient manually"}

# =========================
# SUMMARY (PRO OUTPUT)
# =========================

def summary(services):
    print(f"\n{BOLD}{CYAN}──────── SUMMARY ────────{RESET}")

    if not services:
        print(f"{RED}No open ports found{RESET}")
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

    with open(os.path.join(outdir, "report.json"), "w") as f:
        json.dump(data, f, indent=4)

# =========================
# MAIN
# =========================

def main():
    parser = argparse.ArgumentParser(description="Aurora Recon Framework")

    parser.add_argument("-t", "--target", required=True)
    parser.add_argument("-o", "--output", default=".")
    parser.add_argument("--notes", action="append")

    args = parser.parse_args()

    banner()

    # FIX: workspace ALWAYS uses output dir correctly
    outdir = create_workspace(args.target, args.output)

    print(f"{GRAY}[*] Scanning {args.target}...{RESET}")

    nmap_out = nmap_scan(args.target)

    with open(os.path.join(outdir, "nmap.txt"), "w") as f:
        f.write(nmap_out)

    services = parse_nmap(nmap_out)

    if not services:
        print(f"{RED}[-] No open ports found{RESET}")
        return

    findings = {}

    for s in services:
        if s["port"] == 80:
            findings["http"] = http_enum(args.target, 80)

        elif s["port"] == 22:
            findings["ssh"] = ssh_enum(args.target, 22)

        elif s["port"] == 445:
            findings["smb"] = smb_enum(args.target)

    generate_report(args.target, services, findings, args.notes, outdir)

    summary(services)

    print(f"{GREEN}[+] Done → {outdir}{RESET}")

# =========================

if __name__ == "__main__":
    main()