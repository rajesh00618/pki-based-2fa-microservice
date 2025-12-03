# scripts/create_test_seed.py
import base64
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import secrets

# Load student public key
pub_path = Path("student_public.pem")
if not pub_path.exists():
    raise SystemExit("student_public.pem not found in project root")

pub = serialization.load_pem_public_key(pub_path.read_bytes())

# Example 64-char hex seed (random)
hex_seed = secrets.token_hex(32)  # 32 bytes => 64 hex chars
print("Hex seed (64 chars):", hex_seed)

# Encrypt using RSA OAEP SHA256
cipher = pub.encrypt(
    bytes.fromhex(hex_seed),
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

b64 = base64.b64encode(cipher).decode()
print("\nBase64 encrypted seed (copy this into /decrypt-seed payload):\n")
print(b64)
