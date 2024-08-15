# CrypticGuard

**CrypticGuard** is a powerful file encryption service designed to secure your files on Linux systems. Utilizing a hybrid encryption approach with RSA and AES algorithms, CrypticGuard ensures that your sensitive data remains protected. Think of it as the BitLocker equivalent for Linux. A decryption key is stored securely on your USB drive, making it easy and secure to encrypt and decrypt files.

## Features

- **Hybrid Encryption**: Combines the speed of AES encryption with the security of RSA.
- **USB Key Support**: Use your USB drive as a secure key storage device.
- **Directory Encryption**: Encrypts all files within specified directories.
- **Linux Integration**: Designed specifically for **Linux environments** with **systemd**.

## Installation

### Prerequisites

- **Python 3.10 or newer**: Ensure Python is installed on your system. Download it from the [official Python website](https://www.python.org/).

### Steps to Install

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/mxxim-xd/CrypticGuard.git
   cd CrypticGuard
   ```

2. **Configure Service Files**:

   - Modify the `ExecStart` property in the service files to point to the absolute path of the `doc_crypt.sh` script on your system.
   - Ensure that the `doc_crypt.sh` script references the absolute path of the `doc_crypt.py` file.

3. **Run the Installation Script**:
   Execute the installation script to set up CrypticGuard:
   ```bash
   ./install.sh
   ```

### Post-Installation

- After installation, your service will be set up to start automatically. Ensure your USB key is inserted whenever you need to decrypt files.
