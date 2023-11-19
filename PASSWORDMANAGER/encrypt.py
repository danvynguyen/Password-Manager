import base64
import hashlib
from Crypto.Cipher import AES

class AES256:

    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()
        #run import os, os.urandom(16) then copy and paste into self.ivs
        self.iv = b'\xf1\x85\x19\x8f\xb8\xc0\xf2\xf7\xea3\xeaR\x84\x9c\x8e\xce'

    def encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)

        padding_length = 16 - (len(plaintext) % 16)
        plaintext += chr(padding_length) * padding_length

        ciphertext = cipher.encrypt(plaintext.encode())
        return base64.b64encode(self.iv + ciphertext)
    
    def decrypt(self, ciphertext):
        ciphertext = base64.b64decode(ciphertext)

        iv = ciphertext[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        #remove padding
        plaintext = cipher.decrypt(ciphertext[16:]).decode()
        padding_length = ord(plaintext[-1])
        return plaintext[:-padding_length]