import base64


class BinaryFileError(ValueError):
    """Raised when GitHub blob content is not valid UTF-8 text."""


def decode_file_content(file_data: dict) -> str:
    content = file_data.get("content")
    encoding = file_data.get("encoding")

    if "content" not in file_data:
        raise ValueError("File content is missing")

    if encoding != "base64":
        raise ValueError("Unsupported file encoding")

    try:
        decoded_content = base64.b64decode(content)
        return decoded_content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise BinaryFileError(
            "File content is binary and cannot be decoded as UTF-8"
        ) from error