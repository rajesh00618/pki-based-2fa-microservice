#!/usr/bin/env python3
# scripts/log_2fa_cron.py
import time
from datetime import datetime, timezone
from pathlib import Path
import pyotp
import base64

ROOT = Path.cwd()
DATA_DIR = ROOT / "data"
SEED_PATH = DATA_DIR / "seed.txt"
OUT = ROOT / "cron" / "last_code.txt"

def hex_to_base32(hex_seed: str) -> str:
    raw = bytes.fromhex(hex_seed)
    return base64.b32encode(raw).decode().strip("=")

def gen_code(hex_seed):
    b32 = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(b32, digits=6, interval=30, digest="sha1")
    return totp.now()

def main():
    try:
        if not SEED_PATH.exists():
            OUT.parent.mkdir(parents=True, exist_ok=True)
            OUT.write_text(f"{datetime.now(timezone.utc)} - seed not found\n")
            return
        seed_hex = SEED_PATH.read_text().strip()
        code = gen_code(seed_hex)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        line = f"{ts} - 2FA Code: {code}\n"
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with OUT.open("a", encoding="utf-8") as f:
            f.write(line)
    except Exception as e:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with OUT.open("a", encoding="utf-8") as f:
            f.write(f"{datetime.now(timezone.utc)} - error: {e}\n")

if __name__ == "__main__":
    main()
