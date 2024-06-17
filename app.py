import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QInputDialog
from config.config import Config
from keykeeper import KeyKeeper

class KeyKeeperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('KeyKeeper')
        self.setGeometry(100, 100, 400, 300)

        self.kk = KeyKeeper()
        self.file_path = self.kk.password_file
        self.key = None
        self.salt = None
        self.passwords = {}

        self.main_layout = QVBoxLayout()

        # Label and input for master password
        self.master_label = QLabel('Introduce la clave maestra:')
        self.main_layout.addWidget(self.master_label)
        self.master_input = QLineEdit(self)
        self.master_input.setEchoMode(QLineEdit.Password)
        self.main_layout.addWidget(self.master_input)

        # Button to set master password
        self.master_button = QPushButton('Set Master Password', self)
        self.master_button.clicked.connect(self.set_master_password)
        self.main_layout.addWidget(self.master_button)

        # Label for options
        self.options_label = QLabel('Opciones:')
        self.main_layout.addWidget(self.options_label)

        # Buttons for options
        self.add_button = QPushButton('Añadir contraseña', self)
        self.add_button.clicked.connect(self.add_password)
        self.main_layout.addWidget(self.add_button)

        self.get_button = QPushButton('Obtener contraseña', self)
        self.get_button.clicked.connect(self.get_password)
        self.main_layout.addWidget(self.get_button)

        self.setLayout(self.main_layout)

    def set_master_password(self): #TODO: que sea configurable.
        master_password = self.master_input.text()
        if not os.path.exists(self.file_path):
            self.salt = os.urandom(16) #TODO: que sea configurable.
            self.key = self.kk.generate_key(master_password, self.salt)
            self.kk.save_passwords(self.file_path, {}, self.key, self.salt)
            QMessageBox.information(self, 'Info', 'Archivo de contraseñas creado.')
        else:
            with open(self.file_path, 'rb') as f:
                self.salt = f.read(16)
            self.key = self.kk.generate_key(master_password, self.salt)
            try:
                self.passwords = self.kk.load_passwords(self.file_path, self.key)
                QMessageBox.information(self, 'Info', 'Clave maestra correcta.')
            except:
                QMessageBox.critical(self, 'Error', 'Clave maestra incorrecta.')
                self.key = None

    def add_password(self):
        if self.key is None:
            QMessageBox.warning(self, 'Warning', 'Por favor, establece primero la clave maestra.')
            return

        service, ok = QInputDialog.getText(self, 'Añadir contraseña', 'Introduce el nombre del servicio:')
        if not ok or not service:
            return
        password, ok = QInputDialog.getText(self, 'Añadir contraseña', 'Introduce la contraseña:', QLineEdit.Password)
        if not ok or not password:
            return

        self.passwords[service] = password
        self.kk.save_passwords(self.file_path, self.passwords, self.key, self.salt)
        QMessageBox.information(self, 'Info', 'Contraseña guardada.')

    def get_password(self):
        if self.key is None:
            QMessageBox.warning(self, 'Warning', 'Por favor, establece primero la clave maestra.')
            return

        service, ok = QInputDialog.getText(self, 'Obtener contraseña', 'Introduce el nombre del servicio:')
        if not ok or not service:
            return

        password = self.passwords.get(service)
        if password:
            QMessageBox.information(self, 'Contraseña', f'Contraseña para {service}: {password}')
        else:
            QMessageBox.warning(self, 'Warning', 'Servicio no encontrado.')

def main():
    app = QApplication(sys.argv)
    ex = KeyKeeperApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
