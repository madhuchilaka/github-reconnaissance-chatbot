from dataclasses import dataclass


@dataclass(frozen=True)
class CompanyIdentity:
    name: str
    name_variations: list[str]
    domains: list[str]
    github_organizations: list[str]
    product_names: list[str]
    package_names: list[str]