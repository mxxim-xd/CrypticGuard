#!/bin/bash

echo "PLEASE MAKE SURE TO HAVE YOUR USB PLUGGED IN. YOU'LL NEED IT TO STORE THE PRIVATE KEY!"
echo "AND REMEMBER: NO BACKUP = NO MERCY!"
read -p "Press enter to continue..."

# Generating env vars
echo "Creating env vars..."
read -p "Where should the private key be stored? (on your USB)" key_path

echo -e "KEY_PATH=\"$(pwd)/key.bin\"\nPUBLIC_KEY_PATH=\"$(pwd)/public_key.pem\"\nPRIVATE_KEY_PATH=\"$key_path\"" > .env

# Installing dependencies
echo "Installing dependencies..."
pip3 install pycryptodome
pip3 install dotenv

# Generating symmetric key
echo "Generating symmetric key..."
python3 ./src/sym_key_create.py

# Generating RSA key pair
echo "Generating RSA key pair..."
python3 ./src/key_crypt.py

# Enabling services
echo "Installing services..."
cp ./src/crypt_routine.service /etc/systemd/system/crypt_routine.service
systemctl enable crypt_routine.service

cp ./src/crypt_boot_routine.service /home/$USER/.config/systemd/user/crypt_boot_routine.service
systemctl --user enable crypt_boot_routine.service

echo "RSA keys, symmetric key, env-file and services installed successfully! Make sure to go over them and check if everything is correct."
echo "Don't forget to add the directories you want to encrypt to the target_dir_paths array in the doc_crypt.py file." 
echo "Make sure, that the doc_crypt.sh file only contains absolute paths to the doc_crypt.py file."
echo "Once you reboot your computer the encryption routine will start running in the background."