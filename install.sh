#!/bin/bash

# Prompting user to ensure USB is plugged in
echo "PLEASE MAKE SURE TO HAVE YOUR USB PLUGGED IN. YOU'LL NEED IT TO STORE THE PRIVATE KEY!"
echo "AND REMEMBER: NO BACKUP = NO MERCY!"
read -p "Press enter to continue..."

# Changing paths in service files and doc_crypt.sh
BOOT_SERVICE="./services/crypt_boot_routine.service"
SHUTDOWN_SERVICE="./services/crypt_routine.service"

sed -i "/^ExecStart=/c\ExecStart=$(pwd)/doc_crypt.sh decrypt" "$BOOT_SERVICE"
sed -i "/^ExecStart=/c\ExecStart=$(pwd)/doc_crypt.sh encrypt" "$SHUTDOWN_SERVICE"

# Asking for the private key storage path
read -p "Where should the private key be stored? (.pem file extension) " key_path

# Creating env vars and storing them in .env file
echo "Creating env vars..."
env_file=".env"
cat > "$env_file" <<EOL
KEY_PATH="$(pwd)/key.bin"
PUBLIC_KEY_PATH="$(pwd)/public_key.pem"
PRIVATE_KEY_PATH="$key_path"
MAX_THREADS="64"

# Add the directories you want to encrypt to this array (seperate with comma)
TARGET_DIR_PATHS=""
EOL

# Verifying successful creation of the .env file
if [[ ! -f "$env_file" ]]; then
    echo "Error: Failed to create $env_file."
    exit 1
fi

# Generating symmetric key
echo "Generating symmetric key..."
if ! python3 ./src/sym_key_create.py; then
    echo "Error: Failed to generate symmetric key."
    exit 1
fi

# Generating RSA key pair
echo "Generating RSA key pair..."
if ! python3 ./src/key_crypt.py; then
    echo "Error: Failed to generate RSA key pair."
    exit 1
fi

# Installing services
echo "Installing services..."
services_dir="/etc/systemd/system"
user_services_dir="/home/$USER/.config/systemd/user"

sudo cp ./services/crypt_routine.service "$services_dir/crypt_routine.service"
sudo systemctl enable crypt_routine.service

mkdir -p "$user_services_dir"
cp ./services/crypt_boot_routine.service "$user_services_dir/crypt_boot_routine.service"
systemctl --user enable crypt_boot_routine.service

# Verifying successful service installation
if [[ $? -ne 0 ]]; then
    echo "Error: Failed to install or enable services."
    exit 1
fi

echo "RSA keys, symmetric key, env-file, and services installed successfully! Make sure to review them and check if everything is correct."
echo "Don't forget to add the directories you want to encrypt to the .env file."
echo "Once you reboot your computer, the encryption routine will start running in the background."