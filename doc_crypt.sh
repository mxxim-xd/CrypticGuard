#!/bin/bash

if [ $1 == "decrypt" ]; then
    sleep 10
fi

python3 doc_crypt.sh $1
