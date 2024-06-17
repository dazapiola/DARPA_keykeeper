from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import os
import secrets
import string

def generate_key(password, salt):
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key

def derive_key_from_password(password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def generate_secure_password(length=24):
    characters = string.ascii_letters + string.digits + string.punctuation
    
    password = ''.join(secrets.choice(characters) for i in range(length))
    
    return password

if __name__ == '__main__':
    secure_password = generate_secure_password()
    print(f"Contraseña segura: {secure_password}")
