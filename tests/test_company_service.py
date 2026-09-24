from app.models.company import CompanyIdentity
from app.models.repository import RepositoryCandidate
from app.services.company_service import CompanyService


def test_find_repository_candidates_for_company(monkeypatch):
    company = CompanyIdentity(
        name="Microsoft",
        name_variations=[],
        domains=[],
        github_organizations=["microsoft"],
        product_names=[],
        package_names=[],
    )

    calls = []

    class FakeRepositoryService:
        @staticmethod
        def search_repositories(client, query):
            calls.append((client, query))
            return [
                RepositoryCandidate(
                    full_name=f"example/{query}",
                    owner_login="example",
                    html_url=f"https://github.com/example/{query}",
                    description=None,
                    fork=False,
                    default_branch="main",
                )
            ]

    monkeypatch.setattr(
        "app.services.company_service.RepositoryService",
        FakeRepositoryService,
    )

    results = CompanyService.find_repository_candidates(
        client="fake-client",
        company=company,
    )

    assert calls == [
        ("fake-client", "Microsoft"),
        ("fake-client", "org:microsoft"),
    ]

    assert [candidate.full_name for candidate in results] == [
        "example/Microsoft",
        "example/org:microsoft",
    ]



def test_find_repository_candidates_removes_duplicate_repositories(monkeypatch):
    company = CompanyIdentity(
        name="Microsoft",
        name_variations=[],
        domains=[],
        github_organizations=["microsoft"],
        product_names=[],
        package_names=[],
    )

    repository = RepositoryCandidate(
        full_name="microsoft/vscode",
        owner_login="microsoft",
        html_url="https://github.com/microsoft/vscode",
        description="Visual Studio Code",
        fork=False,
        default_branch="main",
    )

    class FakeRepositoryService:
        @staticmethod
        def search_repositories(client, query):
            return [repository]

    monkeypatch.setattr(
        "app.services.company_service.RepositoryService",
        FakeRepositoryService,
    )

    results = CompanyService.find_repository_candidates(
        client=None,
        company=company,
    )

    assert results == [repository]



def test_build_repository_queries_ignores_empty_identity_values():
    company = CompanyIdentity(
        name="Microsoft",
        name_variations=[],
        domains=["", "microsoft.com", "   "],
        github_organizations=["", "microsoft", "   "],
        product_names=["", "Visual Studio Code", "   "],
        package_names=["", "vscode", "   "],
    )

    queries = CompanyService.build_repository_queries(company)

    assert queries == [
        "Microsoft",
        "org:microsoft",
        "domain:microsoft.com",
        "Visual Studio Code",
        "vscode",
    ]



def test_build_repository_queries_from_name_variations():
    company = CompanyIdentity(
        name="Microsoft",
        name_variations=["Microsoft Corp", "MSFT"],
        domains=[],
        github_organizations=[],
        product_names=[],
        package_names=[],
    )

    queries = CompanyService.build_repository_queries(company)

    assert queries == [
        "Microsoft",
        "Microsoft Corp",
        "MSFT",
    ]


def test_build_repository_queries_removes_duplicate_name_variations():
    company = CompanyIdentity(
        name="Microsoft",
        name_variations=["Microsoft", "MSFT", "Microsoft"],
        domains=[],
        github_organizations=[],
        product_names=[],
        package_names=[],
    )

    queries = CompanyService.build_repository_queries(company)

    assert queries == [
        "Microsoft",
        "MSFT",
    ]



def test_build_repository_queries_strips_identity_values():
    company = CompanyIdentity(
        name="Microsoft",
        name_variations=[" Microsoft Corp "],
        domains=[" microsoft.com "],
        github_organizations=[" microsoft "],
        product_names=[" Visual Studio Code "],
        package_names=[" vscode "],
    )

    queries = CompanyService.build_repository_queries(company)

    assert queries == [
        "Microsoft",
        "Microsoft Corp",
        "org:microsoft",
        "domain:microsoft.com",
        "Visual Studio Code",
        "vscode",
    ]