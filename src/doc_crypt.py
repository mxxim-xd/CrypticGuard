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

# MAX NUMBER OF THREADS TO ASSIGN
MAX_THREADS = int(os.getenv("MAX_THREADS"))


class FileEncryptor:
    # Encrypting the file
    def encrypt_file(self, file_path) -> None:
        with open(file_path, "rb") as f:
            data = f.read() 

        cipher = AES.new(key, AES.MODE_CBC)
        ciphered_data = cipher.encrypt(pad(data, AES.block_size))

        with open(file_path, "wb") as f:
            f.write(cipher.iv) # Initialization vector
            f.write(ciphered_data)

    # Decrypting the file
    def decrypt_file(self, file_path) -> None:
        with open(file_path, "rb") as f:
            iv = f.read(16) # Initialization vector
            data = f.read()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        deciphered_data = unpad(cipher.decrypt(data), AES.block_size)

        with open(file_path, "wb") as f:
            f.write(deciphered_data)

class DirectoryEncryptor(FileEncryptor):
    def __init__(self):
        threads = []

    # Encrypting/Decrypting the directory
    def crypt_dir(self, directory, mode: str) -> None:
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file():
                    self.encrypt_file(entry.path) if mode == "encrypt" else self.decrypt_file(entry.path)
                    print(f"{mode.capitalize()}ed {entry.path}")

                elif entry.is_dir():
                    self.crypt_dir(entry.path, mode)

    def crypt_all_dirs(self, mode: str) -> None:
            threads = self.threads
            #[crypt_dir(target_dir_path, mode) for target_dir_path in target_dir_paths]
            #! FILES IN THE ROOT DIRECTORY ARE NOT ENCRYPTED
            for directory in target_dir_paths:
                subdirs = [os.path.join(directory, entry) for entry in os.listdir(directory) if os.path.isdir(os.path.join(directory, entry))]
                sub_dir_num = len(subdirs)

                if sub_dir_num <= 1:
                    self.crypt_dir(directory, mode)
                    continue
        
                for subdir in subdirs:
                    if len(threads) < MAX_THREADS:
                        thread = threading.Thread(target=self.crypt_dir, args=(subdir, mode,))
                        threads.append(thread)
                        thread.start()
                    else:
                        self.crypt_dir(subdir, mode)
            [thread.join() for thread in threads]
            threads.clear()


def main():
    def load_key():
        with open(KEY_PATH, "rb") as f:
            sym_key = f.read()
        return sym_key

    directoryEncryptor = DirectoryEncryptor()

    try:
        if sys.argv[1] == "encrypt":
            key = load_key()
            directoryEncryptor.crypt_all_dirs("encrypt")
            encrypt_key(KEY_PATH)
        else:
            decrypt_key(KEY_PATH)
            key = load_key()
            directoryEncryptor.crypt_all_dirs("decrypt")
    except FileNotFoundError:
        print("Could not find a key.")
    except ValueError:
        print("Files are encrypted or incorrect decryption.")

if __name__ == "__main__":
    target_dir_paths = os.getenv("TARGET_DIR_PATHS").split(", ")
    if len(target_dir_paths) == 0:
        print("No directories to encrypt or decrypt.")
        sys.exit(0)
    main()
    