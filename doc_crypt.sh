#!/bin/bash

if [ $1 == "decrypt" ]; then
    sleep 10
fi

python3 $(pwd)/src/doc_crypt.py $1
