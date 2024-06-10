from modules.ciphersFiles import decrypt_file
from re import search
from search_key import search_key_path
import uuid
import datetime

class DB:
    def __init__(self):
        key_path = search_key_path()
        self.enc_file_path = key_path + '/private/output/key_secret.enc'
        # Key
        with open(key_path + '/private/.key', 'rb') as keyfile:
            self.key = keyfile.read()
        self._decrypt()

    def _decrypt(self):
        self.decrypt_file = decrypt_file(self.enc_file_path, self.key)
        decoded = self.decrypt_file.decode('utf-8')
        lines = decoded.split('\n')
        return [row for row in lines]

    def query(self, pattern):
        data = self._decrypt()
        for row in data:
            if search(pattern, row):
                if row == None:
                    print("No matches found")
                else:
                    col = row.split(':')
                    return col[2]
            
        return  None
    
    def save(self, description, password):#TODO: falta ver como agregar un valor nuevo automaticamente al archivo cifrado.
        id = uuid.uuid4()
        created = datetime.datetime.now()
        db_file.write(f'{id}:{description}:{password}:{created}')


if __name__ == '__main__':
    db = DB()
    print(f'Hash{db.query("gmail_da")}')
