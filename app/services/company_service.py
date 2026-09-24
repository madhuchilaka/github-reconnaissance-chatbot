from app.models.company import CompanyIdentity
from app.services.repository_service import RepositoryService


class CompanyService:
    @staticmethod
    def build_repository_queries(company: CompanyIdentity) -> list[str]:
        queries = [company.name.strip()]

        queries.extend(
            variation.strip()
            for variation in company.name_variations
            if variation.strip()
        )

        queries.extend(
            f"org:{organization.strip()}"
            for organization in company.github_organizations
            if organization.strip()
        )

        queries.extend(
            f"domain:{domain.strip()}"
            for domain in company.domains
            if domain.strip()
        )

        queries.extend(
            product.strip()
            for product in company.product_names
            if product.strip()
        )

        queries.extend(
            package.strip()
            for package in company.package_names
            if package.strip()
        )

        return list(dict.fromkeys(queries))

    @staticmethod
    def find_repository_candidates(client, company: CompanyIdentity):
        queries = CompanyService.build_repository_queries(company)

        results = []
        seen_repositories = set()

        for query in queries:
            candidates = RepositoryService.search_repositories(
                client,
                query,
            )

            for candidate in candidates:
                if candidate.full_name in seen_repositories:
                    continue

                seen_repositories.add(candidate.full_name)
                results.append(candidate)

        return results