import re

from app.models.domain_indicator import DomainIndicator


DOMAIN_PATTERN = re.compile(
    r"(?:https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
)


def extract_domains(files: list[dict]) -> list[DomainIndicator]:
    domain_evidence: dict[str, list[str]] = {}

    for file_data in files:
        content = file_data.get("content", "")
        path = file_data["path"]

        matches = DOMAIN_PATTERN.findall(content)

        for domain in matches:
            evidence = domain_evidence.setdefault(domain, [])

            if path not in evidence:
                evidence.append(path)

    return [
        DomainIndicator(
            domain=domain,
            evidence=evidence,
        )
        for domain, evidence in domain_evidence.items()
    ]

from app.models.repository_recon import RepositoryReconData


def extract_repository_domains(
    recon_data: RepositoryReconData,
) -> list[DomainIndicator]:
    return extract_domains(recon_data.contents)