from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os
from search_key import search_key_path

class encdec_password:
    def __init__(self):
        key_path = search_key_path()
        with open(key_path + '/private/.key', 'rb') as keyfile:
            self.key = keyfile.read()

    def encrypt_password(self, password):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(password.encode()) + encryptor.finalize()
        return iv + ct
    
    def decrypt_password(self, encrypted_password):
        iv = encrypted_password[:16]
        ct = encrypted_password[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        password = decryptor.update(ct) + decryptor.finalize()
        return password.decode()

if __name__ == '__main__':
    decry = encdec_password()

    password_to_save = input("Enter your secret password: ")
    encrypted_password = decry.encrypt_password(password_to_save)

    print(f'Encrypted password: {encrypted_password}')

    decrypted_password = decry.decrypt_password(encrypted_password)
    print(f'Decrypted password: {decrypted_password}')
