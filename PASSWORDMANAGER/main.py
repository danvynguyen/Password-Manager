from encrypt import AES256
from save import Saver
import os
import string
import random
import smtplib
from email.mime.text import MIMEText

#Set up master password check.
#uncomment the lines 6 and 7 then run Main.py to get masterPasswordCheck variable
#e = AES256("Secret")
#print(e.encrypt("textToMatch"))
#Inspired by: https://www.youtube.com/watch?v=nJtJ1wUACOY  
#(Original features implemented by us: 2-factor authenication and password generator)

#Encrypted master password: "Secret"
masterPasswordCheck = b'8YUZj7jA8vfqM+pShJyOznToSPGx3eOCFikdhfEWS/k='

#generate password function
def generate_password(length=12, use_uppercase=True, use_lowercase=True, use_digits=True, use_special_chars=True):
    characters = ""
            
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation

    if not any([use_uppercase, use_lowercase, use_digits, use_special_chars]):
        raise ValueError("At least one character set should be selected.")

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_random_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_authentication_code(email, code):
    # Set up your email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'joeblokson@gmail.com' #(using my personal email)
    smtp_password = 'dpag uwdn lxzv gyaa'

    # Sender and recipient email addresses
    sender_email = 'joeblokson@gmail.com'
    recipient_email = email

    # Create the email message
    subject = 'Authentication Code'
    body = f'Your authentication code is: {code}'
    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, message.as_string())

saver = Saver("PASSWORDMANAGER\passwords.txt")
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
            # Enter in your email.
            user_email = input("Enter your Email: ")

            # Generate a random authentication code
            authentication_code = generate_random_code()

            # Send the authentication code to the user's email
            send_authentication_code(user_email, authentication_code)

            # Now, prompt the user to enter the received code for verification
            user_input = input("Enter the authentication code received in your email: ")

            # Verify the entered code
            if user_input == authentication_code:
                print("Authentication successful!")
                loggedIn = True
            else:
                print("Authentication failed. Please try again.")

    #clears console
    os.system("cls")

    print("1. Find Password")
    print("2. Add Password")
    print("3. Delete Password")
    print("4. Generate a Password")

    print("\nChoice: ", end="")
    choice = int(input())

    if choice < 1 or choice > 4:
        print("Choice needs to be a number between 1 and 4")
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
    
    elif choice == 4:
        # store all characters in lists 
        
        # Example usage:
        password = generate_password()
        print("Strong Password: " + password)
        input()