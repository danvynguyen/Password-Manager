from encrypt import AES256
from save import Saver
import os

#Set up master password check.
#uncomment the lines 6 and 7 then run Main.py to get masterPasswordCheck variable
#e = AES256("Secret")
#print(e.encrypt("textToMatch"))

#Encrypted master password: "Secret"
masterPasswordCheck = b'8YUZj7jA8vfqM+pShJyOznToSPGx3eOCFikdhfEWS/k='

saver = Saver("passwords.txt")
passwords = saver.read()

loggedIn = False

while True:
    #User login 
    if not loggedIn:
        #user must input masterpassword (In this case, type: "Secret")
        print("Master Password: ", end="")
        masterPassword = input()

        encrypter = AES256(masterPassword)

        if encrypter.encrypt("textToMatch") != masterPasswordCheck:
            print("Password Incorrect")
            input()
            continue
        else:
            loggedIn = True

    #clears console
    os.system("cls")

    print("1. Find Password")
    print("2. Add Password")
    print("3. Delete Password")

    print("\nChoice: ", end="")
    choice = int(input())

    if choice < 1 or choice > 3:
        print("Choice needs to be a number between 1 and 3")
        input()
        continue

    print("Application Name: ", end="")
    app = input()

    if choice == 1:
        for entry in passwords:
            if app in encrypter.decrypt(entry[0]):
                print("\n-----------------------------------------")
                print(f"Application: {encrypter.decrypt(entry[0])}")
                print(f"Password: {encrypter.decrypt(entry[1])}")
        input()
        
    elif choice == 2:
        print("Password: ", end="")
        password = input()

        passwords.append([encrypter.encrypt(app).decode(), encrypter.encrypt(password).decode()])
        saver.save(passwords)

    elif choice == 3:
        for entry in passwords:
            if app == encrypter.decrypt(entry[0]):
                print(f"Are you sure you want to delete '{app} [y/n]: ", end="")
                confirm = input()

                if confirm == "y":
                    del passwords[passwords.index(entry)]
                    saver.save(passwords)

                break