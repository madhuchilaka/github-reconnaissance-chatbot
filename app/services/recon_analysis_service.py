from app.services.file_content_service import decode_file_content
from app.services.file_extractor import extract_repository_files
from app.services.domain_extractor import extract_repository_domains
from app.services.api_extractor import extract_repository_apis
from app.services.security_analysis_service import analyze_security
from app.services.technology_service import TechnologyService
from app.models.recon_analysis import ReconAnalysisResult


class ReconAnalysisService:
    def __init__(self, repository_recon_service) -> None:
        self.repository_recon_service = repository_recon_service

    def load_file_contents(
        self,
        owner: str,
        repo: str,
        files: list[dict],
    ) -> list[dict]:
        loaded_files = []

        for file_data in files:
            path = file_data["path"]

            raw_file = self.repository_recon_service.load_file(
                owner,
                repo,
                path,
            )

            loaded_files.append(
                {
                    "path": path,
                    "content": decode_file_content(raw_file),
                }
            )

        return loaded_files

    def extract_file_indicators(self, recon_data):
        return extract_repository_files(recon_data)

    def extract_domain_indicators(self, recon_data):
        return extract_repository_domains(recon_data)


    def extract_api_indicators(self, recon_data):
        return extract_repository_apis(recon_data)

    def analyze_security(self, files: list[dict]):
        return analyze_security(files)



    def extract_technology_indicators(
        self,
        recon_data,
        owner: str,
        repo: str,
    ):
        technology_service = TechnologyService(
            file_loader=self.repository_recon_service.load_file,
            owner=owner,
            repo=repo,
        )

        return technology_service.extract_technologies(recon_data)


    def analyze_repository(
        self,
        owner: str,
        repo: str,
    ) -> ReconAnalysisResult:
        recon_data = self.repository_recon_service.collect_repository_for_analysis(
            owner,
            repo,
        )

        file_indicators = self.extract_file_indicators(
            recon_data,
        )

        loaded_files = self.load_file_contents(
            owner,
            repo,
            recon_data.contents,
        )

        technology_indicators = self.extract_technology_indicators(
            recon_data,
            owner,
            repo,
        )

        domain_indicators = self.extract_domain_indicators(
            recon_data,
        )

        api_indicators = self.extract_api_indicators(
            recon_data,
        )

        security_findings = self.analyze_security(
            loaded_files,
        )

        return ReconAnalysisResult(
            files=file_indicators,
            technologies=technology_indicators,
            domains=domain_indicators,
            apis=api_indicators,
            security_findings=security_findings,
        )