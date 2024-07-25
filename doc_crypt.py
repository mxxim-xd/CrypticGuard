from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from key_crypt import encrypt_key, decrypt_key
from dotenv import load_dotenv
import os
import sys
import threading

load_dotenv()
KEY_PATH = os.getenv("KEY_PATH")

# Generate key
"""salt = get_random_bytes(32)
key = PBKDF2("fgdgfddgf", salt, dkLen=32)

# Export key
with open("key.bin", "wb") as f:
    f.write(key)"""


# Encrypting the file
def encrypt_file(file_path):
    with open(file_path, "rb") as f:
        data = f.read() 

    cipher = AES.new(key, AES.MODE_CBC)
    ciphered_data = cipher.encrypt(pad(data, AES.block_size))

    with open(file_path, "wb") as f:
        f.write(cipher.iv) # Initialization vector
        f.write(ciphered_data)

# Decrypting the file
def decrypt_file(file_path):
    with open(file_path, "rb") as f:
        iv = f.read(16) # Initialization vector
        data = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    deciphered_data = unpad(cipher.decrypt(data), AES.block_size)

    with open(file_path, "wb") as f:
        f.write(deciphered_data)

# Encrypting/Decrypting the directory
def crypt_dir(directory, mode):
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                encrypt_file(entry.path) if mode == "encrypt" else decrypt_file(entry.path)
                print(f"{mode.capitalize()}ed {entry.path}")

            elif entry.is_dir():
                crypt_dir(entry.path, mode)

def load_key():
    with open(KEY_PATH, "rb") as f:
        sym_key = f.read()
    return sym_key



def main():
    threads = []
    global key

    def crypt_all_dirs(mode):
        #[crypt_dir(target_dir_path, mode) for target_dir_path in target_dir_paths]
        for directory in target_dir_paths:
            thread = threading.Thread(target=crypt_dir, args=(directory, mode,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    try:
        if sys.argv[1] == "encrypt":
            key = load_key()
            crypt_all_dirs("encrypt")
            encrypt_key(KEY_PATH)
        else:
            decrypt_key(KEY_PATH)
            key = load_key()
            crypt_all_dirs("decrypt")
    except FileNotFoundError:
        print("Could not find a key.")
    except ValueError:
        print("Files are encrypted.")

if __name__ == "__main__":
    target_dir_paths = []

    if len(target_dir_paths) == 0:
        print("No directories to encrypt/decrypt.")
        sys.exit(1)

    main()
    