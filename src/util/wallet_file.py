import json
from pathlib import Path

from util.wallet_html import WalletUtility
from web3.wallet import Wallet


class WalletFile:
    """Wallet file class to create wallet files (HTML/JSON) from a specified wallet."""

    EXT_HTML: str = "html"
    EXT_JSON: str = "json"
    INDENT: int = 4

    wallet: Wallet | None = None
    path: str | None = None
    file_name_base: str | None = None
    html: str | None = None

    def __init__(self, wallet: Wallet) -> None:
        """Create a new wallet file."""
        self.wallet = wallet
        self.html = WalletUtility.create(wallet)
        self.file_name_base = self.wallet.address  # type: ignore  # noqa: PGH003

    def save(self, path: str | None = None) -> None:
        """Save the wallet as HTML file and JSON vault file."""
        base_name = self.get_base_name(path)

        with Path(f"{base_name}.{self.EXT_HTML}").open("w") as html_file:
            html_file.write(str(self.html))

        with Path(f"{base_name}.{self.EXT_JSON}").open("w") as json_file:
            json_file.write(self.get_vault_file())

    def get_base_name(self, path: str | None) -> str:
        """Return the base name (without file extension) for this wallet file."""
        if not path:
            self.path = "."
        else:
            self.path = path

        if self.path.endswith("/"):
            self.path = self.path[:-1]

        return f"{self.path}/{self.file_name_base}"

    def get_wallet_file(self) -> str:
        """Return the HTML wallet file content."""
        return str(self.html)

    def get_vault_file(self) -> str:
        """Return the JSON vault file content."""
        return json.dumps(self.wallet.vault, indent=self.INDENT)  # type: ignore  # noqa: PGH003
