from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import os

class securePasswordManager:
    def __init__(self):
        from search_key import search_key_path
        key_path = search_key_path()

        with open(key_path + '/private/.salt', 'rb') as salt_f:
            self.salt = salt_f.read()

    def _derive_key_from_password(self, password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def encrypt_password(self, password, user_password):
        key = self._derive_key_from_password(user_password)
        f = Fernet(key)
        encrypted_password = f.encrypt(password.encode())
        return encrypted_password

    def decrypt_password(self, encrypted_password, user_password):
        key = self._derive_key_from_password(user_password)
        f = Fernet(key)
        decrypted_password = f.decrypt(encrypted_password)
        return decrypted_password.decode()

if __name__ == "__main__":
    password = "my_secure_password"
    user_password = input("Ingrese su clave para cifrar la contraseña: ")
    spm = securePasswordManager()
    encrypted_password = spm.encrypt_password(password, user_password)
    print(f"Contraseña cifrada: {encrypted_password}")

    user_password_to_decrypt = input("Ingrese su clave para descifrar la contraseña: ")
    try:
        decrypted_password = spm.decrypt_password(encrypted_password, user_password_to_decrypt)
        print(f"Contraseña descifrada: {decrypted_password}")
    except Exception as e:
        print("La clave ingresada es incorrecta o los datos fueron manipulados.")
