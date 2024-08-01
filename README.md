# File Encryption Service

This is a file encryption service that encrypts files in directories through a combination of the AES and RSA encryption algorithms. It is meant to be used as a sort of BitLocker for Linux. You have a key on your USB-Drive which is used to decrypt your files.

## Installation

To install the file encryption service, you will need to have Python installed on your system. You can download Python from the official website: https://www.python.org/

Make sure to change the ExecStart property in the services files to the path of the doc_crypt.sh file on your system.
Also use the absolute path of the doc_crypt.py file in the doc_crypt.sh file.

Then run the following script:

```bash
./install.sh
```
