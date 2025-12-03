from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generate RSA private key (4096 bit, exponent 65537)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096
)

# Write private key to file student_private.pem
with open("student_private.pem", "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Extract and write public key student_public.pem
public_key = private_key.public_key()
with open("student_public.pem", "wb") as f:
    f.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("RSA 4096-bit keypair generated successfully!")
