#!/bin/bash

if [ $1 == "decrypt" ]; then
    sleep 10
fi

python3 doc_crypt.py $1

# THIS SCRIPT RUNS AS PART OF THE crypt_routine.service with links in 
# /etc/systemd/system/halt.target.wants
# /etc/systemd/system/reboot.target.wants
# /etc/systemd/system/shutdown.target.wants
# /home/maxim/.config/systemd/user/default.target.wants
# SERVICES ARE STORED IN /etc/systemd/system/ AS:
# /etc/systemd/system/crypt_routine.service
# /home/maxim/.config/systemd/user/crypt_boot_routine.service