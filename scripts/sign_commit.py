# scripts/sign_commit.py
import subprocess
import base64
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# 1) get latest commit hash
commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip()
print("commit hash:", commit.decode())

# 2) load student private key
priv_path = Path("student_private.pem")
if not priv_path.exists():
    raise SystemExit("student_private.pem not found")
priv = serialization.load_pem_private_key(priv_path.read_bytes(), password=None)

# 3) sign commit hash using RSA-PSS SHA256
signature = priv.sign(
    commit,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)

# 4) load instructor public key
instr_pub_path = Path("instructor_public.pem")
if not instr_pub_path.exists() or instr_pub_path.stat().st_size == 0:
    raise SystemExit("instructor_public.pem missing or empty — need real instructor public key.")

instr_pub = serialization.load_pem_public_key(instr_pub_path.read_bytes())

# 5) encrypt signature with instructor public key (OAEP SHA256)
encrypted = instr_pub.encrypt(
    signature,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# 6) encode base64 and save
b64 = base64.b64encode(encrypted).decode()
Path("proof_signature.b64").write_text(b64)

print("\nEncrypted signature saved to proof_signature.b64\n")
print("-----BEGIN BASE64-----")
print(b64)
print("-----END BASE64-----")
