from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

salt = get_random_bytes(32)
key = PBKDF2("something", salt, dkLen=32)

# Export key
with open("key.bin", "wb") as f:
    f.write(key)

print("Key generated and saved to key.bin")