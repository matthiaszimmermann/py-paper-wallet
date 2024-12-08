# Python Paper Wallet

## Overview
The initial layout of this repository is based on [github.com/matthiaszimmermann/python-uv].

## TODO
- Improve documentation
- Add logging support

## Appendix

### Use Console
```sh
uv run python
```

```sh
from web3.wallet import Wallet
from util.wallet_file import WalletFile
w = Wallet.create()
wf = WalletFile(w)

# create the paper wallet HTML and vault JSON files
wf.save()
```

### Run Tests
```sh
pytest
```
