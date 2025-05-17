# This import Fernet,aclass from the cryptography module
# it provides encryption and descryption using a secret key
from cryptography.fernet import Fernet
import os
import json


class PasswordManager:
    def __init__(self):
        self.key_file="secret.keys"
        self.password_file="passwords.json"
        self.key=self.load_or_create_key()
        self.fernet=Fernet(self.key)
        self.passwords=self.load_passwords()

    def load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file,"rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file,"wb")as f:
                f.write(key)
            return key
    
    def load_passwords(self):
        if os.path.exists(self.password_file):
            with open(self.password_file,"r")as f:
                return json.load(f)
        return{}
    
    def save_passwords(self):
        with open(self.password_file,'w') as f:
            json.dump(self.passwords,f)

    def add_password(self,account,password):
        encrypted_pw =self.fernet.encrypt(password.encode()).decode()
        self.passwords[account] = encrypted_pw
        self.save_passwords()
        print("The password added  Successfully")

    def view_passwords(self):
        if not self.passwords:
            print("No Passwords Here or not saved")
            return
        for account,encrypted in self.passwords.items():
            decrypted = self.fernet.decrypt(encrypted.encode()).decode()
            print(f"{account}:{decrypted}")

    def search_account(self,account):
        if account in self.passwords:
            decrypted =self.fernet.decrypt(self.passwords[account].encode()).decode()
            print(f"Found-{account}:{decrypted}")
        else:
            print("Account not Found")

    def delete_account(self,account):
        if account in self.passwords:
           del self.passwords[account]
           self.save_passwords()
           print("Account Deleted")
        else:
            print("Account not Found")


#-------------------------------
#cpi
#------------------------------
if __name__ == "__main__":
    manager = PasswordManager()

    while True:
        print("\n====Password Manager Menu ===")
        print("1.Add Password")
        print("2.View Password")
        print("3.Search Account")
        print("4.Delete Account")
        print("5.Exit")

        choice=input("Enter your choice:")

        if choice == '1':
            acc = input("Enter your Account Name: ")
            pw =input("Enter your Password")
            manager.add_password(acc,pw)

        elif choice == '2':
            manager.view_passwords()

        elif choice == '3':
            acc = input("Enter your Account Name to search :")
            manager.search_account(acc)
        
        elif choice == '4':
            acc = input("Enter your Account name to delete: ")
            manager.delete_account(acc)

        elif choice == '5':
            print("Exciting ..stay secure")
            break

        else:
            print("Invalid choice")