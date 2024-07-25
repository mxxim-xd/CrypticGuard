from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from dotenv import load_dotenv
import os

load_dotenv()
private_key_path = os.getenv("PRIVATE_KEY_PATH")
public_key_path = os.getenv("PUBLIC_KEY_PATH")

def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_key(key_path):
    with open(key_path, 'rb') as f:
        data = f.read()

    public_key = RSA.import_key(open(public_key_path).read())
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher.encrypt(data)

    with open(key_path, 'wb') as f:
        f.write(encrypted_data)

def decrypt_key(key_path):
    with open(key_path, 'rb') as f:
        encrypted_data = f.read()

    private_key = RSA.import_key(open(private_key_path).read())
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_data = cipher.decrypt(encrypted_data)

    with open(key_path, 'wb') as f:
        f.write(decrypted_data)


if __name__ == "__main__":
    # Check if RSA keys exist, if not generate a new pair
    try:
        private_key = open(private_key_path, "r").read()
        public_key = open(public_key_path, "r").read()
    except FileNotFoundError:
        private_key, public_key = generate_key_pair()
        # Save the generated keys to files
        with open(private_key_path, "wb") as f:
            f.write(private_key)
        with open(public_key_path, "wb") as f:
            f.write(public_key)
