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
    def __init__(self, key):
        self.key = key

    # Encrypting the file
    def encrypt_file(self, file_path) -> None:
        with open(file_path, "rb") as f:
            data = f.read() 

        cipher = AES.new(self.key, AES.MODE_CBC)
        ciphered_data = cipher.encrypt(pad(data, AES.block_size))

        with open(file_path, "wb") as f:
            f.write(cipher.iv) # Initialization vector
            f.write(ciphered_data)

    # Decrypting the file
    def decrypt_file(self, file_path) -> None:
        with open(file_path, "rb") as f:
            iv = f.read(16) # Initialization vector
            data = f.read()

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        deciphered_data = unpad(cipher.decrypt(data), AES.block_size)

        with open(file_path, "wb") as f:
            f.write(deciphered_data)

class DirectoryEncryptor(FileEncryptor):
    def __init__(self, key, mode: str):
        super().__init__(key)
        self.mode: str = mode
        self.threads: list[threading.Thread] = []

    def add_thread(self, thread: threading.Thread) -> None: 
        self.threads.append(thread)
        thread.start()

    # Encrypting/Decrypting the directory
    def crypt_dir(self, directory: str) -> None:
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file():
                    self.encrypt_file(entry.path) if self.mode == "encrypt" else self.decrypt_file(entry.path)
                    print(f"{self.mode.capitalize()}ed {entry.path}")

                elif entry.is_dir():
                    self.crypt_dir(entry.path)

    def initialize_crypt_process(self, dir_paths: list[str]) -> None:
        for directory in dir_paths:
            thread = threading.Thread(target=self.crypt_all_dirs, args=([directory], True,))
            self.add_thread(thread)

        [thread.join() for thread in self.threads]
        self.threads.clear()

    """
    The function crypt_all_dirs processes a list of directories for encryption or decryption, using multi-threading for efficiency.
    It begins by iterating through each directory, separating its contents into subdirectories and files.
    If there are files, a thread is created to encrypt or decrypt them based on the current mode (encrypt or decrypt),
    and the thread is added to a thread management system. If the get_layer flag is set to True,
    the function recursively processes all subdirectories at this level, then proceeds to handle subdirectories without further recursion.
    For each subdirectory, a thread is created to process its contents if the number of active threads is below MAX_THREADS.
    Otherwise, the subdirectory is processed synchronously.
    This approach ensures efficient parallel processing while respecting the thread limit.

    @param dir_paths: List[str] - A list of strings, each representing a directory path to be processed.
    @param get_layer: bool - A boolean flag indicating whether to process subdirectories at the current level.
    @return None
    """

    def crypt_all_dirs(self, dir_paths: list[str], get_layer: bool) -> None:
        for directory in dir_paths:
            subdirs: list[str] = [os.path.join(directory, entry) for entry in os.listdir(directory) if os.path.isdir(os.path.join(directory, entry))]
            leftover_files: list[str] = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
            
            if len(leftover_files) > 0:
                crypt_leftover = lambda: [self.encrypt_file(path) if self.mode == "encrypt" else self.decrypt_file(path) for path in leftover_files]
                thread = threading.Thread(target=crypt_leftover)
                self.add_thread(thread)

            if get_layer:
                self.crypt_all_dirs(subdirs, False)
                continue

            for directory in subdirs:
                if len(self.threads) < MAX_THREADS:
                    thread = threading.Thread(target=self.crypt_dir, args=(directory,))
                    self.add_thread(thread)
                else:
                    self.crypt_dir(directory)
        print("Process completed")

def main():
    def load_key() -> str:
        with open(KEY_PATH, "rb") as f:
            sym_key = f.read()
        return sym_key

    try:
        if sys.argv[1] == "encrypt":
            key = load_key()
            DirectoryEncryptor(key, "encrypt").initialize_crypt_process(target_dir_paths)
            encrypt_key(KEY_PATH)
        else:
            decrypt_key(KEY_PATH)
            key = load_key()
            DirectoryEncryptor(key, "decrypt").initialize_crypt_process(target_dir_paths)
    except FileNotFoundError:
        print("Could not find a key.")
    except ValueError:
        print("Files are encrypted or incorrect decryption.")

if __name__ == "__main__":
    target_dir_paths: list[str] = os.getenv("TARGET_DIR_PATHS").split(", ")
    if len(target_dir_paths) == 0:
        print("No directories to encrypt or decrypt.")
        sys.exit(0)
    main()
    