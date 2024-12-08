from eth_account.hdaccount import ETHEREUM_DEFAULT_PATH  # noqa: INP001
from eth_account.signers.local import LocalAccount

from web3.wallet import Wallet

# see https://gist.github.com/kendricktan/9cb7debcec62848722f36944518d55f9
TRUFFLE_DEFAULT_MNEMONIC = (
    "candy maple cake sugar pudding cream honey rich smooth crumble sweet treat"
)

DEFAULT_ADDRESSES = [
    "0x627306090abaB3A6e1400e9345bC60c78a8BEf57",
    "0xf17f52151EbEF6C7334FAD080c5704D77216b732",
    "0xC5fdf4076b8F3A5357c5E395ab970B5B54098Fef",
    "0x821aEa9a577a9b44299B9c15c88cf3087F3b5544",
    "0x0d1d4e623D10F9FBA5Db95830F7d3839406C6AF2",
    "0x2932b7A2355D6fecc4b5c0B6BD44cC31df247a2e",
    "0x2191eF87E392377ec08E7c08Eb105Ef5448eCED5",
    "0x0F4F2Ac550A1b4e2280d04c21cEa7EBD822934b5",
    "0x6330A553Fc93768F612722BB8c2eC78aC90B3bbc",
    "0x5AEDA56215b167893e80B4fE645BA6d5Bab767DE",
]

DEFAULT_KEYS = [
    "0xc87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3",
    "0xae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f",
    "0x0dbbe8e4ae425a6d2687f1a7e3ba17bc98c673636790f1b8ad91193c05875ef1",
    "0xc88b703fb08cbea894b6aeff5a544fb92e78a18e19814cd85da83b71f772aa6c",
    "0x388c684f0ba1ef5017716adb5d21a053ea8e90277d0868337519f97bede61418",
    "0x659cbb0e2411a44db63778987b1e22153c086a95eb6b18bdf89de078917abc63",
    "0x82d052c865f5763aad42add438569276c00d3d88a2d062d36b2bae914d58b8c8",
    "0xaa3680d5d48a8283413f7a108367c7299ca73f553735860a87b08f39395618b7",
    "0x0f62d96d6675f32685bbdb8ac13cda7c23436f63efbb9d07700d8669ff12b7c4",
    "0x8d5366123cb560bb606379f90a0bfd4769eecc0557f1b362dcae9012b548b1e5",
]

TEST_PASSWORD = "0123456789ab"  # noqa: S105


def test_wallet_create_no_args() -> None:  # noqa: D103
    w = Wallet.create(password=TEST_PASSWORD)

    assert w is not None
    assert isinstance(w.mnemonic, str)
    assert isinstance(w.address, str)
    assert isinstance(w.path, str)
    assert isinstance(w.index, int)
    assert isinstance(w.password, str)
    assert isinstance(w.account, LocalAccount)
    assert isinstance(w.vault, dict)

    # check mnemonic length
    assert Wallet.WORDS_DEFAULT == 12
    assert len(w.mnemonic.split(" ")) == Wallet.WORDS_DEFAULT

    # check path and index
    assert Wallet.INDEX_DEFAULT == 0
    assert w.path == ETHEREUM_DEFAULT_PATH
    assert w.index == Wallet.INDEX_DEFAULT

    # check pass phrase
    assert len(w.password) == 12
    assert w.password == TEST_PASSWORD

    # check address
    assert len(w.address) == 42

    # check that mnemonic leads to same address
    w_from_mnemonic = Wallet.from_mnemonic(w.mnemonic)
    assert w_from_mnemonic.mnemonic == w.mnemonic
    assert w_from_mnemonic.address == w.address
    assert w_from_mnemonic.index == w.index
    assert w_from_mnemonic.path == w.path


def test_wallet_create_from_mnemonic() -> None:  # noqa: D103
    w = Wallet.from_mnemonic(TRUFFLE_DEFAULT_MNEMONIC)

    assert w.mnemonic == TRUFFLE_DEFAULT_MNEMONIC
    assert w.index == 0
    assert w.path == ETHEREUM_DEFAULT_PATH
    assert w.address == DEFAULT_ADDRESSES[0]
    assert w.account.key.to_0x_hex() == DEFAULT_KEYS[0]  # type: ignore  # noqa: PGH003
    assert isinstance(w.vault, dict)

    for i in range(1, 5):
        check_address_for_index(i)


def test_wallet_create_from_vault() -> None:  # noqa: D103
    w = Wallet.create(password=TEST_PASSWORD)
    w_reconstructed = Wallet.from_vault(w.vault, password=w.password)

    assert w_reconstructed.password == w.password
    assert w_reconstructed.account.key.to_0x_hex() == w.account.key.to_0x_hex()  # type: ignore  # noqa: PGH003
    assert w_reconstructed.address == w.address


def check_address_for_index(index: int) -> None:  # noqa: D103
    w = Wallet.from_mnemonic(TRUFFLE_DEFAULT_MNEMONIC, index=index)
    assert w.mnemonic == TRUFFLE_DEFAULT_MNEMONIC
    assert w.address == DEFAULT_ADDRESSES[index]
    assert w.account.key.to_0x_hex() == DEFAULT_KEYS[index]  # type: ignore  # noqa: PGH003

    assert w.index == index
    assert Wallet.index_from_path(str(w.path)) == index
    assert isinstance(w.vault, dict)
