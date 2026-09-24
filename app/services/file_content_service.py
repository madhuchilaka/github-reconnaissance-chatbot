import base64


def decode_file_content(file_data: dict) -> str:
    content = file_data.get("content")
    encoding = file_data.get("encoding")

    if not content:
        raise ValueError("File content is missing")

    if encoding != "base64":
        raise ValueError("Unsupported file encoding")

    return base64.b64decode(content).decode("utf-8")