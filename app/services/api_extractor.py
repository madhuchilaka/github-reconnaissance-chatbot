import re

from app.models.api_indicator import ApiIndicator
from app.models.repository_recon import RepositoryReconData


API_URL_PATTERN = re.compile(
    r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s""''<>)]*)?'
    r'|'
    r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/[^\s""''<>)]*'
)

HTTP_METHOD_PATTERN = re.compile(
    r'\b(?:requests|httpx)\.(get|post|put|patch|delete|head|options)\s*\(',
    re.IGNORECASE,
)


def extract_apis(files: list[dict]) -> list[ApiIndicator]:
    api_evidence: dict[str, list[str]] = {}
    api_methods: dict[str, str | None] = {}

    for file_data in files:
        content = file_data.get("content", "")
        path = file_data["path"]

        for match in API_URL_PATTERN.finditer(content):
            url = match.group(0)

            evidence = api_evidence.setdefault(url, [])

            if path not in evidence:
                evidence.append(path)

            method = _extract_method_for_url(content, match.start())

            if url not in api_methods or api_methods[url] is None:
                api_methods[url] = method

    return [
        ApiIndicator(
            url=url,
            method=api_methods[url],
            evidence=evidence,
        )
        for url, evidence in api_evidence.items()
    ]


def _extract_method_for_url(content: str, url_start: int) -> str | None:
    preceding_content = content[:url_start]

    method_matches = list(HTTP_METHOD_PATTERN.finditer(preceding_content))

    if not method_matches:
        return None

    return method_matches[-1].group(1).upper()



def extract_repository_apis(
    recon_data: RepositoryReconData,
) -> list[ApiIndicator]:
    return extract_apis(recon_data.contents)