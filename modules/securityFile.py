from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

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

if __name__ == '__main__':
    passwrod = "12345"
    salt = os.urandom(16)
    key = generate_key(passwrod, salt)
    print(f'key: {key}, salt {salt}')    
    # save the key and salt securely
    with open("key.key", "wb") as key_file:
        key_file.write(key)

    with open("salt.salt", "wb") as salt_file:
        salt_file.write(salt)
