from pqcrypto.sign import rainbow
import base64
import json

#TODO: Crer un nuevo cifrado para guardar las contraseñdeberías
# con el uso de post-quantum
# https://pqcrypto.eu.org/deliverables/d2.4.pdf
# https://pypi.org/project/pqcrypto/

# Generar claves pública y privada
public_key = rainbow.generate_keypair()

def save_password(service, password, private_key, filename='passwords.json'):
    # Cifrar la contraseña (aquí usamos la firma como cifrado simplificado)
    message = f"{service}:{password}".encode()
    signature = rainbow.sign(private_key, message)

    # Codificar la firma y la contraseña en base64 para almacenarla
    encoded_signature = base64.b64encode(signature).decode()
    encoded_message = base64.b64encode(message).decode()

    # Guardar en un archivo JSON
    try:
        with open(filename, 'r') as file:
            passwords = json.load(file)
    except FileNotFoundError:
        passwords = {}

    passwords[service] = {'message': encoded_message, 'signature': encoded_signature}
    
    with open(filename, 'w') as file:
        json.dump(passwords, file, indent=4)

def get_password(service, public_key, filename='passwords.json'):
    try:
        with open(filename, 'r') as file:
            passwords = json.load(file)
    except FileNotFoundError:
        print("No se encontró el archivo de contraseñas.")
        return None

    if service not in passwords:
        print("Servicio no encontrado.")
        return None

    # Obtener la firma y el mensaje almacenados
    encoded_signature = passwords[service]['signature']
    encoded_message = passwords[service]['message']

    # Decodificar la firma y el mensaje desde base64
    signature = base64.b64decode(encoded_signature)
    message = base64.b64decode(encoded_message)

    # Verificar la firma
    if rainbow.verify(public_key, message, signature):
        return message.decode().split(':')[1]
    else:
        print("Firma no válida. La contraseña no pudo ser verificada.")
        return None

def main():
    master_password = input("Introduce la clave maestra: ")

    # Generar clave privada a partir de la clave maestra
    private_key = rainbow.generate_private_key()  # En una aplicación real, deberías derivar esto de la clave maestra

    while True:
        print("\n1. Añadir contraseña")
        print("\n2. Obtener contraseña")
        print("\n3. Salir")
        choice = input("Elige una opción: ")

        if choice == '1':
            service = input("Introduce el nombre del servicio: ")
            password = input("Introduce la contraseña: ")
            save_password(service, password, private_key)
            print("Contraseña guardada.")

        elif choice == '2':
            service = input("Introduce el nombre del servicio: ")
            password = get_password(service, public_key)
            if password:
                print(f"Contraseña para {service}: {password}")

        elif choice == '3':
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
