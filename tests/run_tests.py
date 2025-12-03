# tests/run_tests.py
import subprocess, json, time, os
from pathlib import Path
import requests

BASE = "http://127.0.0.1:8080"
ROOT = Path.cwd()

def run_create_seed():
    print("Generating test seed (scripts/create_test_seed.py)...")
    out = subprocess.check_output(["py", "scripts/create_test_seed.py"], text=True)
    blob = out.strip().splitlines()[-1].strip()
    print("seed blob length:", len(blob))
    return blob

def post_decrypt(blob):
    print("\nPosting to /decrypt-seed ...")
    r = requests.post(f"{BASE}/decrypt-seed", json={"encrypted_seed": blob}, timeout=5)
    print("status:", r.status_code)
    print("response:", r.text)
    return r

def gen_code():
    print("\nCalling /generate-2fa ...")
    r = requests.get(f"{BASE}/generate-2fa", timeout=5)
    print("status:", r.status_code)
    print("response:", r.text)
    return r.json()

def verify_code(code):
    print("\nVerifying code", code)
    r = requests.post(f"{BASE}/verify-2fa", json={"code": code}, timeout=5)
    print("status:", r.status_code)
    print("response:", r.text)
    return r.json()

def test_cron_log():
    print("\nRunning cron logger script once...")
    subprocess.check_call(["py", "scripts/log_2fa_cron.py"])
    time.sleep(0.5)
    log_file = ROOT / "cron" / "last_code.txt"
    if not log_file.exists():
        raise SystemExit("cron/last_code.txt not found")
    lines = log_file.read_text().strip().splitlines()
    print("Latest cron log:", lines[-1])
    return True

def main():
    print("=== PKI 2FA Automated Test ===")

    blob = run_create_seed()

    r = post_decrypt(blob)
    if r.status_code != 200:
        raise SystemExit("decrypt-seed failed")

    seed_path = ROOT / "data" / "seed.txt"
    if not seed_path.exists():
        raise SystemExit("seed.txt missing after decrypt")
    print("seed saved OK:", seed_path.read_text().strip()[:20] + "...")

    data = gen_code()
    code = data["code"]

    result = verify_code(code)
    if not result.get("valid"):
        raise SystemExit("verify-2fa returned false")

    test_cron_log()

    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY 🎉")

if __name__ == "__main__":
    main()
