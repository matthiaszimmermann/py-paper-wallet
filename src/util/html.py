import base64
from io import BytesIO


class HtmlUtility:
    """Utility class to build Ethereum paper wallet HTML files."""

    NEWLINE = "\n"

    HTML = "html"
    HEAD = "head"
    TITLE = "title"
    STYLE = "style"
    BODY = "body"
    DIV = "div"
    H2 = "h2"
    P = "p"
    FOOTER = "footer"

    @staticmethod
    def add_title(buf: list, title: str) -> None:
        """Add the HTML title element."""
        HtmlUtility.add_element_with_content(buf, HtmlUtility.TITLE, title)

    @staticmethod
    def add_styles(buf: list, *styles: str) -> None:
        """Add the style element."""
        HtmlUtility.add_open_elements_with_class(buf, HtmlUtility.STYLE)
        for style in styles:
            buf.append(style)
            buf.append(HtmlUtility.NEWLINE)
        HtmlUtility.add_close_elements(buf, HtmlUtility.STYLE)

    @staticmethod
    def add_header2(buf: list, title: str) -> None:
        """Add an H2 element."""
        HtmlUtility.add_element_with_content(buf, HtmlUtility.H2, title)

    @staticmethod
    def add_paragraph(buf: list, paragraph: str, css_class: str | None = None) -> None:
        """Add a paragraph element."""
        HtmlUtility.add_element_with_content(buf, HtmlUtility.P, paragraph, css_class)

    @staticmethod
    def add_content(buf: list, content: str) -> None:
        """Add more text."""
        if content:
            buf.append(content)

    @staticmethod
    def add_element_with_content(
        buf: list, element: str, content: str, css_class: str | None = None
    ) -> None:
        """Add an element of the specified class."""
        if not content:
            return
        if not element:
            msg = "Tag of element to add must not be empty or null"
            raise ValueError(msg)
        HtmlUtility.add_open_elements_with_class(buf, element, css_class=css_class)
        buf.append(content)
        HtmlUtility.add_close_elements(buf, element)

    @staticmethod
    def add_encoded_image(
        buf: list, image: BytesIO, css_class: str | None = None
    ) -> None:
        """Add the specified (encoded) image."""
        try:
            data = image.read()
            HtmlUtility.add_encoded_image_bytes(buf, data, css_class)
        except Exception as e:
            msg = "Failed to load content from file input stream:"
            raise RuntimeError(msg, e) from e

    @staticmethod
    def add_encoded_image_bytes(
        buf: list, image_file: bytes, css_class: str | None = None
    ) -> None:
        """Add the specified (encoded) image."""
        encoded_file = HtmlUtility.get_encoded_bytes(image_file)
        encoded_image = (
            f'<img class="{css_class}" src="data:image/png;base64,{encoded_file}">\n'
        )
        buf.append(encoded_image)

    @staticmethod
    def add_open_div(buf: list, *class_attributes: str) -> None:
        """Add a div opening element."""
        classes = " ".join(class_attributes)
        buf.append(f'<{HtmlUtility.DIV} class="{classes}">\n')

    @staticmethod
    def add_close_div(buf: list) -> None:
        """Add a div closing element."""
        HtmlUtility.add_close_elements(buf, HtmlUtility.DIV)

    @staticmethod
    def add_open_footer(buf: list, *class_attributes: str) -> None:
        """Add a footer opening element."""
        classes = " ".join(class_attributes)
        buf.append(f'<{HtmlUtility.FOOTER} class="{classes}">\n')

    @staticmethod
    def add_close_footer(buf: list) -> None:
        """Add a footer closing element."""
        HtmlUtility.add_close_elements(buf, HtmlUtility.FOOTER)

    @staticmethod
    def add_open_elements(buf: list, *elements: str) -> None:
        """Add a sequence of opening elements."""
        HtmlUtility.add_open_elements_with_class(buf, *elements)

    @staticmethod
    def add_open_elements_with_class(
        buf: list, *elements: str, css_class: str | None = None
    ) -> None:
        """Add a sequence of opening elements."""
        for element in elements:
            buf.append(HtmlUtility.to_open_element(element, css_class))  # noqa: PERF401

    @staticmethod
    def add_close_elements(buf: list, *elements: str) -> None:
        """Add a sequence of closing elements."""
        for element in elements:
            buf.append(HtmlUtility.to_close_element(element))  # noqa: PERF401

    @staticmethod
    def get_encoded_bytes(data: bytes) -> str:
        """Return the provided bytes in b64 encoded format."""
        return base64.b64encode(data).decode("utf-8")

    @staticmethod
    def to_open_element(element: str, css_class: str | None = None) -> str:
        """Return an opening element."""
        if not css_class:
            return f"<{element}>\n"
        return f'<{element} class="{css_class}">\n'

    @staticmethod
    def to_close_element(element: str) -> str:
        """Return a closing element."""
        return f"</{element}>\n"
