from modules.search_key import search_key_path

class Config :
    def __init__(self):
        key_path = search_key_path()
        folder_path = '/private/'
        # Archivo para almacenar la clave de cifrado
        # TODO: Agregar la key para el cifrado de archivo.
        self.KEY_FILE = key_path + folder_path + 'secret.key'
        # Archivo para almacenar las contraseñas cifradas
        self.PASSWORD_FILE = key_path + folder_path + 'qwerty.enc'
