from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import os

class RSACipher :
    def __init__(self, key_size=2048, key_folder='cipher/rsa/keys'):
        self.key_size = key_size
        self.key_folder = key_folder
        self.private_key_path = os.path.join(self.key_folder, "private.pem")
        self.public_key_path = os.path.join(self.key_folder, "public.pem")
        os.makedirs(self.key_folder, exist_ok=True)
    
    def generate_keys(self):
        key = RSA.generate(self.key_size)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        
        with open(self.private_key_path, "wb") as priv_file:
            priv_file.write(private_key)
        with open(self.public_key_path, "wb") as pub_file:
            pub_file.write(public_key)
    
    def load_keys(self):
        try:
            with open(self.private_key_path, "rb") as priv_file:
                private_key = RSA.import_key(priv_file.read())
            with open(self.public_key_path, "rb") as pub_file:
                public_key = RSA.import_key(pub_file.read())
            return private_key, public_key
        except FileNotFoundError:
            raise Exception("Key files not found. Generate keys first.")
    
    def encrypt(self, message, key):
        cipher = PKCS1_OAEP.new(key)
        encrypted_message = cipher.encrypt(message.encode())
        return encrypted_message
    
    def decrypt(self, ciphertext, key):
        cipher = PKCS1_OAEP.new(key)
        decrypted_message = cipher.decrypt(ciphertext)
        return decrypted_message.decode()
    
    def sign(self, message, private_key):
        h = SHA256.new(message.encode())
        signature = pkcs1_15.new(private_key).sign(h)
        return signature
    
    def verify(self, message, signature, public_key):
        h = SHA256.new(message.encode())
        try:
            pkcs1_15.new(public_key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False