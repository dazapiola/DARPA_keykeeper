from modules.db import DB
from modules.encdec_password import encdec_password

def main():
    db = DB()
    
    while True:
        print("1. Save a new password")
        print("2. Retrieve a password")
        print("3. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            description = input("Enter name or description: \n")
            password = input("Enter password: \n")
            db.save(description, password) # TODO
        elif choice == '2':
            description = input("Enter name or description: ")
            password = db.query(description)
            if password:
                print(f"Password: {password}")
                encdec = encdec_password()
                encdec.decrypt_password(encrypted_password, key)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
