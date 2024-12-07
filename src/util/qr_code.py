from io import BytesIO

import qrcode


class QrCodeUtility:
    """Utility class to create QR code images."""

    IMAGE_FILE_TYPE = "PNG"
    ENCODING_TYPE = "UTF-8"

    @staticmethod
    def content_to_png_bytes(content: str, size: int) -> bytes:
        """Turn the provided string into a QR code image."""
        try:
            # Create QR code instance with custom configurations
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_L,  # type: ignore  # noqa: PGH003
                box_size=10,  # Adjusts the box size
                border=0,  # No border, similar to setting margin=0 in Java
            )
            qr.add_data(content)
            qr.make(fit=True)

            # Generate image
            image = qr.make_image(fill_color="black", back_color="white")
            image = image.resize((size, size))  # type: ignore # Resize to the specified size  # noqa: PGH003

            # Convert to byte array
            with BytesIO() as output:
                image.save(output, format=QrCodeUtility.IMAGE_FILE_TYPE)
                return output.getvalue()

        except Exception as e:
            msg = "Failed to produce image byte array"
            raise RuntimeError(msg) from e
