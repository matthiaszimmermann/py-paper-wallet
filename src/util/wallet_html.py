import json
from datetime import UTC, datetime
from pathlib import Path

from util.html import HtmlUtility
from util.qr_code import QrCodeUtility
from web3.wallet import Wallet


class WalletUtility(HtmlUtility):
    """Utility class to create HTML documents for provided wallets."""

    VERSION = "0.1.0"
    REPOSITORY = "https://github.com/matthiaszimmermann/py-paper-wallet"

    TITLE = "Ethereum Paper Wallet"
    ETHEREUM_LOGO = "./resources/ethereum_logo.png"

    CSS_CLEARFIX = "clearfix"
    CSS_ADDRESS_ROW = "address-row"
    CSS_COLUMN = "column"
    CSS_FILL = "fill-right"
    CSS_NOTES = "notes"
    CSS_CONTENT = "content"
    CSS_CAPTION = "caption"
    CSS_FOOTER = "footer-content"
    CSS_IMG_ADDRESS = "img-address"
    CSS_IMG_WALLET = "img-wallet"

    CSS_STYLES = [  # noqa: RUF012
        "html * { font-family:Verdana, sans-serif; }",
        f'.{CSS_CLEARFIX}::after {{ content: ""; clear:both; display:table; }}',
        f".{CSS_ADDRESS_ROW} {{ background-color:#eef; }}",
        "@media screen {",
        f".{CSS_COLUMN} {{ float:left; padding: 15px; }}",
        f".{CSS_FILL} {{ overflow:auto; padding:15px; }}",
        f".{CSS_NOTES} {{ height:256px; background-color:#fff; }}",
        f".{CSS_CONTENT} {{ padding:15px; background-color:#efefef; font-family:monospace; }}",  # noqa: E501
        f".{CSS_CAPTION} {{ margin-top:6px; font-size:smaller;}}",
        f".{CSS_FOOTER} {{ font-size:small; }}",
        f".{CSS_IMG_ADDRESS} {{ display:block; height:256px; }}",
        f".{CSS_IMG_WALLET} {{ display:block; height:400px }}",
        "}",
        "@media print {",
        f".{CSS_COLUMN} {{ float:left; padding:8pt; }}",
        f".{CSS_FILL} {{ overflow:auto; padding:8pt; }}",
        f".{CSS_NOTES} {{ height:100pt; border-style:solid; border-width:1pt; }}",
        f".{CSS_CONTENT} {{ background-color:#efefef; font-family:monospace; font-size:6pt }}",  # noqa: E501
        f".{CSS_CAPTION} {{ margin-top:2pt; font-size:smaller;}}",
        f".{CSS_FOOTER} {{ font-size:6pt; }}",
        f".{CSS_IMG_ADDRESS} {{ display:block; height:100pt; }}",
        f".{CSS_IMG_WALLET} {{ display:block; height:180pt }}",
        "}",
    ]

    @staticmethod
    def create(wallet: Wallet) -> str:
        """Create a paper wallet HTML for the specified wallet object.

        The HTML content is returned as a 'str' object.
        """
        html = []

        # Header
        HtmlUtility.add_open_elements(html, HtmlUtility.HTML, HtmlUtility.HEAD)
        HtmlUtility.add_title(html, WalletUtility.TITLE)
        HtmlUtility.add_styles(html, " ".join(WalletUtility.CSS_STYLES))
        HtmlUtility.add_close_elements(html, HtmlUtility.HEAD)

        # Body
        HtmlUtility.add_open_elements(html, HtmlUtility.BODY)
        HtmlUtility.add_header2(html, WalletUtility.TITLE)

        # Add first row
        HtmlUtility.add_open_div(
            html, WalletUtility.CSS_CLEARFIX, WalletUtility.CSS_ADDRESS_ROW
        )

        # Ethereum logo
        HtmlUtility.add_open_div(html, WalletUtility.CSS_COLUMN)
        logo = WalletUtility.get_file_bytes(WalletUtility.ETHEREUM_LOGO)
        HtmlUtility.add_encoded_image_bytes(html, logo, WalletUtility.CSS_IMG_ADDRESS)
        HtmlUtility.add_close_div(html)

        # Account address
        HtmlUtility.add_open_div(html, WalletUtility.CSS_COLUMN)
        address_qr_code = QrCodeUtility.content_to_png_bytes(str(wallet.address), 256)
        HtmlUtility.add_encoded_image_bytes(
            html, address_qr_code, WalletUtility.CSS_IMG_ADDRESS
        )
        HtmlUtility.add_paragraph(html, "QR Code Address", WalletUtility.CSS_CAPTION)
        HtmlUtility.add_close_div(html)

        # Notes
        HtmlUtility.add_open_div(html, WalletUtility.CSS_FILL)
        HtmlUtility.add_open_div(html, WalletUtility.CSS_NOTES)
        HtmlUtility.add_close_div(html)
        HtmlUtility.add_paragraph(html, "Notes", WalletUtility.CSS_CAPTION)
        HtmlUtility.add_close_div(html)

        HtmlUtility.add_close_div(html)

        # Add second row
        HtmlUtility.add_open_div(html, WalletUtility.CSS_CLEARFIX)

        # # QR code for wallet file
        vault_file_content = json.dumps(wallet.vault)
        HtmlUtility.add_open_div(html, WalletUtility.CSS_COLUMN)
        wallet_qr_code = QrCodeUtility.content_to_png_bytes(vault_file_content, 400)
        HtmlUtility.add_encoded_image_bytes(
            html, wallet_qr_code, WalletUtility.CSS_IMG_WALLET
        )
        HtmlUtility.add_paragraph(
            html, "QR Code Wallet File", WalletUtility.CSS_CAPTION
        )
        HtmlUtility.add_close_div(html)

        # Address, passphrase, wallet file, file name
        HtmlUtility.add_open_div(html, WalletUtility.CSS_FILL)
        WalletUtility.add_wallet_details(html, wallet, vault_file_content)
        HtmlUtility.add_close_div(html)

        # Add footer content
        reference = f"[{WalletUtility.REPOSITORY}] v{WalletUtility.VERSION}"
        footer = f"Created with EPW Generator {reference}"
        HtmlUtility.add_open_footer(html, WalletUtility.CSS_FOOTER)
        HtmlUtility.add_content(html, footer)
        HtmlUtility.add_close_footer(html)

        HtmlUtility.add_close_elements(html, HtmlUtility.BODY, HtmlUtility.HTML)

        return "".join(html)

    @staticmethod
    def add_wallet_details(html: list, wallet: Wallet, vault_file_content: str) -> None:
        """Add address, mnemonic, path, pass phrase and the vault."""
        details = [
            (wallet.address, "Address"),
            (WalletUtility.get_creation_time_utc(), "Creation Timestamp"),
            (wallet.mnemonic, "Mnemonic"),
            (wallet.path, "BIP 44 Path"),
            (wallet.password, "Pass Phrase"),
            (vault_file_content.replace(',"', ', "'), "Vault File"),
        ]

        for content, caption in details:
            HtmlUtility.add_paragraph(html, caption, WalletUtility.CSS_CAPTION)
            HtmlUtility.add_open_div(html, WalletUtility.CSS_CONTENT)
            HtmlUtility.add_content(html, content)
            HtmlUtility.add_close_div(html)

    @staticmethod
    def get_creation_time_utc() -> str:
        """Return the current UTC time as str.

        Example: 2024-12-07 19:20:11 UTC.
        """
        now_utc = datetime.now(UTC)
        return now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")

    @staticmethod
    def get_file_bytes(file_path: str) -> bytes:
        """Return the file content as bytes."""
        try:
            file = Path(file_path)
            with file.open("rb") as f:
                return f.read()
        except Exception as e:
            msg = f"Failed to read file: {file_path}"
            raise RuntimeError(msg) from e
