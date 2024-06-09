from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def encrypt_file(file_path, key):
    iv = os.urandom(16) # initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(file_path, 'rb') as f:
        file_data = f.read()

    encrypted_data = encryptor.update(file_data) + encryptor.finalize()

    with open(file_path + ".enc", 'wb') as f:
        f.write(iv + encrypted_data)
    print(f'[+]File {file_path} encrypted successfully!')

def decrypt_file(encrypted_file_path, key, save=False):
    with open(encrypted_file_path, 'rb') as f:
        iv = f.read(16)
        encrypted_data = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    if save:
        original_file_path = encrypted_file_path.replace(".enc", ".dec")
        with open(original_file_path, 'wb') as f:
            f.write(decrypted_data)
        print(f'File {encrypted_file_path} decrypted successfully!')

    return decrypted_data



if __name__ == '__main__':
    # Key
    with open("key.key", 'rb') as keyfile:
        key = keyfile.read()

    # encrypt
    file_path = "test.secret"
    #encrypt_file(file_path, key)

    # decrypted
    enc_file_path = "test.secret.enc"
    tecrypt_file(enc_file_path, key)
