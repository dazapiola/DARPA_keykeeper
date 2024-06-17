import os
import json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from config.config import Config

class KeyKeeper():
    def __init__(self):
        self.config = Config()
        self.salt_n = 12
        self.password_file = self.config.PASSWORD_FILE

# Función para generar una clave a partir de la clave maestra
    def generate_key(self, master_password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(master_password.encode())

# Función para cifrar los datos
    def encrypt_data(self, key, data):
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        encrypted_data = aesgcm.encrypt(nonce, data.encode(), None)
        return nonce + encrypted_data

# Función para descifrar los datos
    def decrypt_data(self, key, encrypted_data):
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ciphertext, None).decode()

# Función para guardar las contraseñas en un archivo
    def save_passwords(self, file_path, passwords, key, salt):
        encrypted_passwords = self.encrypt_data(key, json.dumps(passwords))
        with open(file_path, 'wb') as f:
            f.write(salt + encrypted_passwords)

# Función para cargar las contraseñas desde un archivo
    def load_passwords(self, file_path, key):
        with open(file_path, 'rb') as f:
            data = f.read()
        salt = data[:16]
        encrypted_passwords = data[16:]
        decrypted_passwords = self.decrypt_data(key, encrypted_passwords)
        return json.loads(decrypted_passwords)

# Función principal
def main():
    kk = KeyKeeper()
    file_path = kk.password_file
    master_password = input("Introduce la clave maestra: ")

    # Si el archivo de contraseñas no existe, crear uno nuevo
    if not os.path.exists(file_path):
        salt = os.urandom(16)
        key = kk.generate_key(master_password, salt)
        passwords = {}
        kk.save_passwords(file_path, passwords, key, salt)
        print("Archivo de contraseñas creado.")
    else:
        with open(file_path, 'rb') as f:
            salt = f.read(16)
        key = kk.generate_key(master_password, salt)
        try:
            passwords = kk.load_passwords(file_path, key)
        except:
            print("Clave maestra incorrecta.")
            return

    while True:
        print("\n1. Añadir contraseña")
        print("\n2. Obtener contraseña")
        print("\n3. Salir")
        choice = input("Elige una opción: ")

        if choice == '1':
            service = input("Introduce el nombre del servicio: ")
            password = input("Introduce la contraseña: ")
            passwords[service] = password
            kk.save_passwords(file_path, passwords, key, salt)
            print("Contraseña guardada.")

        elif choice == '2':
            service = input("Introduce el nombre del servicio: ")
            if service in passwords:
                print(f"Contraseña para {service}: {passwords[service]}")
            else:
                print("Servicio no encontrado.")

        elif choice == '3':
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
