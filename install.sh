#!/bin/bash

echo "PLEASE MAKE SURE TO HAVE YOUR USB PLUGGED IN. YOU'LL NEED IT TO STORE THE PRIVATE KEY!"

echo "Creating env vars..."
read -p "Where should the private key be stored? (on your USB)" key_path

echo -e "KEY_PATH=\"$(pwd)/key.bin\"\nPUBLIC_KEY_PATH=\"$(pwd)/public_key.pem\"\nPRIVATE_KEY_PATH=\"$key_path\"" > .env

echo "Generating symmetric key..."
python3 ./src/sym_key_create.py

echo "Generating RSA key pair..."
python3 ./src/key_crypt.py