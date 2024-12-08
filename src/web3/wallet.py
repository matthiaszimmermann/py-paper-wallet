from typing import Any

from eth_account import Account
from eth_account.hdaccount import ETHEREUM_DEFAULT_PATH
from eth_account.signers.local import LocalAccount
from eth_account.types import Language

from util.password import generate_password


class Wallet:
    """Simple class for wallet creation."""

    VALID_NUM_WORDS = [12, 15, 18, 21, 24]  # noqa: RUF012
    WORDS_DEFAULT = 12

    LANGUAGE_DEFAULT = Language.ENGLISH
    PATH_PARTS = 6
    INDEX_DEFAULT = 0

    password: str
    vault: dict[str, Any]
    mnemonic: str | None
    address: str
    account: LocalAccount | None
    language: Language | None
    path: str | None
    index: int | None

    def __init__(self) -> None:
        """Create a new wallet.

        Do not use this function to create a new wallet.
        Use the static creator funcitons instead.
        """
        Account.enable_unaudited_hdwallet_features()

        self.password = ""
        self.vault = {}
        self.mnemonic = None
        self.address = ""
        self.account = None
        self.language = None
        self.path = ETHEREUM_DEFAULT_PATH
        self.index = Wallet.INDEX_DEFAULT

    @classmethod
    def create(
        cls,
        words: int = WORDS_DEFAULT,
        language: Language = LANGUAGE_DEFAULT,
        index: int = INDEX_DEFAULT,
        password: str = generate_password(),
    ) -> "Wallet":
        """Create a new wallet."""
        Wallet.validate_index(index)
        Wallet.validate_num_words(words)

        wallet = Wallet()
        wallet.language = language
        wallet.index = index

        if index > 0:
            wallet.path = ETHEREUM_DEFAULT_PATH[:-1] + str(index)

        (wallet.account, wallet.mnemonic) = Account.create_with_mnemonic(
            "", words, language, wallet.path
        )

        wallet.address = wallet.account.address  # type: ignore  # noqa: PGH003
        wallet.password = password
        wallet.vault = wallet.account.encrypt(password)  # type: ignore  # noqa: PGH003

        return wallet

    @staticmethod
    def from_mnemonic(
        mnemonic: str,
        index: int = INDEX_DEFAULT,
        password: str = generate_password(),
        path: str = ETHEREUM_DEFAULT_PATH,
    ) -> "Wallet":
        """Create a new wallet from a provided mnemonic."""
        Wallet.validate_mnemonic(mnemonic)
        Wallet.validate_index(index)

        wallet = Wallet()
        wallet.mnemonic = mnemonic
        wallet.index = index
        wallet.path = path

        # modify path if index is provided
        if index:
            wallet.path = "/".join(path.split("/")[:-1]) + f"/{index}"

        wallet.password = password
        wallet.account = Account.from_mnemonic(mnemonic, account_path=wallet.path)
        wallet.vault = wallet.account.encrypt(password)  # type: ignore  # noqa: PGH003
        wallet.address = wallet.account.address  # type: ignore  # noqa: PGH003

        return wallet

    @staticmethod
    def from_vault(vault: dict[str, Any], password: str) -> "Wallet":
        """Create a new wallet from a vault dict."""
        wallet = Wallet()
        wallet.password = password
        wallet.vault = vault
        wallet.account = Account.from_key(Account.decrypt(vault, password=password))
        wallet.address = wallet.account.address  # type: ignore  # noqa: PGH003

        return wallet

    @staticmethod
    def index_from_path(path: str) -> int:
        """Extract index from provided path string."""
        Wallet.validate_path(path)
        return int(path.split("/")[-1])

    @staticmethod
    def validate_path(path: str) -> None:
        """Perform basic sanity checks.

        Raise an error if provided path is invalid.
        """
        if not isinstance(path, str):
            msg = "Provided path is not of type str"
            raise TypeError(msg)

        parts = len(path.split("/"))
        if parts != Wallet.PATH_PARTS:
            msg = (
                f"Path format invalid, {Wallet.PATH_PARTS} parts expected, got {parts}"
            )
            raise ValueError(msg)

    @staticmethod
    def validate_mnemonic(mnemonic: str) -> None:
        """Perform basic sanity checks.

        Raise an error if provided mnemonic is invalid.
        """
        if not isinstance(mnemonic, str):
            msg = "Provided mnemonic is not of type str"
            raise TypeError(msg)

        Wallet.validate_num_words(len(mnemonic.split()))

    @staticmethod
    def validate_num_words(words: int) -> None:
        """Check that provided number of words is valid.

        Raise an error if provided number of words is invalid.
        """
        if not isinstance(words, int):
            msg = "Provided number of words is not of type int"
            raise TypeError(msg)

        if words not in Wallet.VALID_NUM_WORDS:
            msg = f"Provided number of words is not in {Wallet.VALID_NUM_WORDS}"
            raise ValueError(msg)

    @staticmethod
    def validate_index(index: int) -> None:
        """Perform basic sanity checks.

        Raise an error if provided index is undefined or invalid.
        """
        if not isinstance(index, int):
            msg = "Provided index is not of type int"
            raise TypeError(msg)

        if index < 0:
            msg = "Provided index is negative"
            raise ValueError(msg)
