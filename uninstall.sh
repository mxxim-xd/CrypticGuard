#!/bin/bash


# TODO Warnings
read -p "MAKE SURE TO DECRYPT EVERYTHING THAT WAS ENCRYPTED BEFORE RUNNING THIS SCRIPT!"

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
    exit 1
fi

# Removing keys from usb drive

read -p "Do you wish to delete your key stored on your usb drive? (Y/N): " key_removal

echo "Make sure to plug in your usb drive!"
read -p "Press enter to continue..."

# Reads out the .env file and stores the filtered content in a variable
#PUBLIC_KEY_PATH=$(cat .env | grep "PUBLIC_KEY_PATH")

