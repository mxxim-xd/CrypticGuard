import os

key = os.urandom(32)

# Export key
with open("key.bin", "wb") as f:
    f.write(key)

print("Key generated and saved to key.bin")