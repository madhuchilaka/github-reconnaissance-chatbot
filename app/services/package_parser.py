import json


def parse_package_json(content: str) -> dict:
    try:
        data = json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError("Invalid package.json content") from error

    if not isinstance(data, dict):
        raise ValueError("package.json content must be a JSON object")

    return data