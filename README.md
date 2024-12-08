# Python Paper Wallet

## Overview

This repository provides Python based software to create Ethereum paper wallets.

### What is an Ethereum Paper Wallet?

An Ethereum paper wallet is a form of offline storage for your Ethereum holdings where the private key and the corresponding public address are physically printed (or otherwise recorded) on a piece of paper.

Key Characteristics:

* **Offline Storage**: Because the private key never needs to be kept on an internet-connected device, paper wallets are immune to online hacking attempts.
* **No Hardware Required**: Unlike hardware wallets or USB drives, a paper wallet only requires a secure place to store a piece of paper.
* **Vulnerability to Physical Damage or Loss**: While safe from digital theft, paper wallets are susceptible to physical risks—if the paper is damaged, lost, or destroyed, you could lose access to your funds. Proper protection (lamination, backups, secure safes) is often recommended.
* **No Native Transaction Functionality**: To send funds, you need to import the paper wallet’s private key into a software wallet or another Ethereum-compatible tool. The paper wallet itself is just the static record of your keys.

The risk of pyhical damage or loss is not specific to paper wallets. It also applies to laptops that hold web based wallets like Metamask, and hardware wallets like Tezos.

In essence, an Ethereum paper wallet provides a low-tech, offline method of securing your cryptocurrency, relying on physical security measures rather than complex hardware or software-based protections.

*Source: Shameless copy job using ChatGPT. The content seemed fine and only the remark about physical damage and loss of other wallets was added.*


### Previous Work
The functionality is close to the [previous setup](https://github.com/matthiaszimmermann/ethereum-paper-wallet) based on Java.
The initial layout of this repository is based on [python-uv](github.com/matthiaszimmermann/python-uv).

## Preparation

To use this repository the following software is required:

- Git
- Docker
- VSCode

## Initial Setup
1. Clone repository into directory of your choice
1. Open VSCode in this directory
1. Run Devcontainer setup

## Run Tests
```sh
pytest
```

## Python Console in VSCode

Open a terminal in VSCode and type the following command.

```sh
uv run python
```

Run the following commands in the python shell to create a paper wallet
```python
from web3.wallet import Wallet
from util.wallet_file import WalletFile
w = Wallet.create()
wf = WalletFile(w)

# create the paper wallet HTML and vault JSON files
wf.save()
```

## Create the Docker Image

In a shell (outside of VSCode):
1. Cd into the main directory of the py-paper-wallet repository
1. Run the following command

```sh
docker build -t py-paper-wallet .
```

## Run a Container

In a shell (outside of VSCode):
1. Create a sub-directory `wallets` in a directory of your choice
1. Start an interactive Docker container with the following command

```sh
docker run --rm -it -v $(pwd)/wallets:/app/wallets py-paper-wallet
```

Inside the container start the Python console

```sh
uv run python
```

Now create your wallets using the container
1. Disconnect your computer from the internet/wifi/...
1. Create a new paper wallet using the following commands

```python
from web3.wallet import Wallet
from util.wallet_file import WalletFile
w = Wallet.create()
wf = WalletFile(w)

# save the paper wallet HTML and vault JSON files into the linkes wallets directory
wf.save('wallets')
```

In the `wallets` you will now find all the saved wallet HTML files and vault JSON files.

Then
1. Quit the Python shell using `<ctrl>-d`
2. Quit the container using `<ctrl>-d`
3. Print and verify your paper wallets in the `wallets` directory
4. Delete the wallet HTML file and make sure that you empty the trash too
5. You may switch your internet connection on again
