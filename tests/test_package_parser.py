from app.services.package_parser import parse_package_json


def test_parse_package_json():
    content = """
    {
        "name": "example-app",
        "dependencies": {
            "react": "^19.0.0"
        }
    }
    """

    result = parse_package_json(content)

    assert result["name"] == "example-app"
    assert result["dependencies"]["react"] == "^19.0.0"


def test_parse_package_json_rejects_invalid_json():
    content = "{invalid json}"

    try:
        parse_package_json(content)
    except ValueError as error:
        assert str(error) == "Invalid package.json content"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )


def test_parse_package_json_rejects_non_object():
    content = '["react"]'

    try:
        parse_package_json(content)
    except ValueError as error:
        assert str(error) == "package.json content must be a JSON object"
    else:
        raise AssertionError(
            "Expected ValueError was not raised"
        )