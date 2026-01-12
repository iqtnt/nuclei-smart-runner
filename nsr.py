#!/usr/bin/env python3
import subprocess
import sys
import time
import argparse
from pathlib import Path

NUCLEI_BIN = "nuclei"
BLOCK_LINE = "unsigned templates for scan. Use with caution"

def parse_args():
    parser = argparse.ArgumentParser(
        description="Nuclei runner (stats + banner enabled, block one warning line only)"
    )
    parser.add_argument(
        "-l", "--list",
        required=True,
        help="File containing target domains"
    )
    parser.add_argument(
        "-server",
        required=True,
        help="OAST server (e.g. xxxx.oast.online)"
    )
    return parser.parse_args()

def get_first_target(file_path):
    lines = file_path.read_text().splitlines()
    return lines[0].strip() if lines else None

def remove_first_target(file_path):
    lines = file_path.read_text().splitlines()
    file_path.write_text("\n".join(lines[1:]) + ("\n" if len(lines) > 1 else ""))

def run_nuclei(target, oast_server):
    cmd = f"""
{NUCLEI_BIN} -u "{target}" \
-severity low,medium,high,critical \
-stats \
-iserver {oast_server} \
| grep -v "{BLOCK_LINE}" \
| tee -a vuln.txt \
| notify
"""
    subprocess.run(cmd, shell=True, executable="/bin/bash")

def notify_finished():
    msg = "✅ Scan completed. All domains have been scanned. Please review results and run the tool again."
    subprocess.run(f'echo "{msg}" | notify', shell=True)

def main():
    args = parse_args()
    targets_file = Path(args.list)

    if not targets_file.exists():
        print(f"[!] Targets file not found: {targets_file}")
        sys.exit(1)

    print("[*] Nuclei scan started\n")

    while True:
        target = get_first_target(targets_file)

        if not target:
            notify_finished()
            print("[✓] All targets scanned")
            break

        print(f"[*] Starting scan: {target}")

        try:
            run_nuclei(target, args.server)
            print(f"[✓] Scan finished: {target}")
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user")
            sys.exit(0)
        except Exception as e:
            print(f"[!] Error: {e}")

        remove_first_target(targets_file)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
