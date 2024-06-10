from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
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

def generate_secure_password(length=24):
    characters = string.ascii_letters + string.digits + string.punctuation
    
    password = ''.join(secrets.choice(characters) for i in range(length))
    
    return password

if __name__ == '__main__':
    #passwrod = "12345"
    #salt = os.urandom(16)
    #key = generate_key(passwrod, salt)
    #print(f'key: {key}, salt {salt}')    
    # save the key and salt securely
    #with open("key.key", "wb") as key_file:
    #    key_file.write(key)

    #with open("salt.salt", "wb") as salt_file:
    #    salt_file.write(salt)
    secure_password = generate_secure_password()
    print(f"Contraseña segura: {secure_password}")
