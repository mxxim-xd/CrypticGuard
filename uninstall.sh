#!/bin/bash


# TODO Warnings
read -p "MAKE SURE TO DECRYPT EVERYTHING THAT WAS ENCRYPTED BEFORE RUNNING THIS SCRIPT! "

# Uninstalling services
services_dir="/etc/systemd/system"
user_services_dir="/home/$USER/.config/systemd/user"

sudo systemctl disable crypt_routine.service
sudo rm "$services_dir/crypt_routine.service"

systemctl --user disable crypt_boot_routine.service
rm "$user_services_dir/crypt_boot_routine.service"


# Verifying successful service removal
if [[ $? -ne 0 ]]; then
    echo "Error: Failed to uninstall services."
fi

# Removing keys from usb drive

read -p "Do you wish to delete your keys stored on your usb drive? (Y/N) default[Y]: " answer

if [[ $answer == "n" || $answer == "N" ]] then
    echo "Successfully deleted services"
    exit 1
fi

echo "Make sure to plug in your USB drive!"
read -p "Press enter to continue..."

ENV_FILE=".env"

# Extract KEY_PATH
KEY_PATH=$(grep "^KEY_PATH=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"')

# Extract PUBLIC_KEY_PATH
PUBLIC_KEY_PATH=$(grep "^PUBLIC_KEY_PATH=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"')

# Extract PRIVATE_KEY_PATH
PRIVATE_KEY_PATH=$(grep "^PRIVATE_KEY_PATH=" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"')

# Output the results
rm $KEY_PATH || { echo "Error: Failed to remove $KEY_PATH"; }
rm $PUBLIC_KEY_PATH || { echo "Error: Failed to remove $PUBLIC_KEY_PATH"; }
rm $PRIVATE_KEY_PATH || { echo "Error: Failed to remove $PRIVATE_KEY_PATH"; }

echo "Successfully deleted services and keys"