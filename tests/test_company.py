from app.models.company import CompanyIdentity


def test_company_identity_creation():
    company = CompanyIdentity(
        name="Microsoft",
        name_variations=[],
        domains=["microsoft.com"],
        github_organizations=["microsoft"],
        product_names=["Visual Studio Code"],
        package_names=[],
    )

    assert company.name == "Microsoft"
    assert company.domains == ["microsoft.com"]
    assert company.github_organizations == ["microsoft"]
    assert company.product_names == ["Visual Studio Code"]
    assert company.package_names == []