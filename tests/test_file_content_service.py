from app.services.file_content_service import decode_file_content


def test_decode_file_content():
    file_data = {
        "content": "SGVsbG8gV29ybGQ=",
        "encoding": "base64",
    }

    result = decode_file_content(file_data)

    assert result == "Hello World"


def test_decode_file_content_rejects_missing_content():
    file_data = {
        "encoding": "base64",
    }

    try:
        decode_file_content(file_data)
    except ValueError as error:
        assert str(error) == "File content is missing"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_decode_file_content_rejects_unsupported_encoding():
    file_data = {
        "content": "Hello World",
        "encoding": "utf-8",
    }

    try:
        decode_file_content(file_data)
    except ValueError as error:
        assert str(error) == "Unsupported file encoding"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )