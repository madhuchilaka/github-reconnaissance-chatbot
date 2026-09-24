from app.models.repository_recon import RepositoryReconData
from app.models.technology_indicator import TechnologyIndicator
from app.services.file_content_service import decode_file_content
from app.services.package_parser import parse_package_json
from app.services.technology_extractor import (
    detect_cpp,
    detect_docker,
    detect_express,
    detect_go,
    detect_java,
    detect_javascript,
    detect_kotlin,
    detect_nodejs,
    detect_php,
    detect_python,
    detect_react,
    detect_ruby,
    detect_rust,
    detect_swift,
    detect_typescript,
)
    

class TechnologyService:

    def __init__(
        self,
        file_loader=None,
        owner: str | None = None,
        repo: str | None = None,
    ) -> None:
        self.file_loader = file_loader
        self.owner = owner
        self.repo = repo

    def extract_technologies(
        self,
        recon_data: RepositoryReconData,
    ) -> list[TechnologyIndicator]:
        files = recon_data.contents

        detectors = [
            detect_python,
            detect_javascript,
            detect_typescript,
            detect_java,
            detect_go,
            detect_rust,
            detect_cpp,
            detect_php,
            detect_ruby,
            detect_swift,
            detect_kotlin,
            detect_docker,
            detect_nodejs,
        ]

        indicators = []

        for detector in detectors:
            result = detector(files)

            if result is not None:
                indicators.append(result)

        package_files = [
            file_data
            for file_data in files
            if file_data.get("name", "").lower() == "package.json"
        ]

        if package_files and self.file_loader is not None:
            package_file = package_files[0]
            package_path = package_file["path"]
            package_data = self.parse_package_data(package_path)

            for detector in (detect_react, detect_express):
                result = detector(package_path, package_data)

                if result is not None:
                    indicators.append(result)

        return indicators


    def parse_package_data(self, path: str) -> dict:
        if self.file_loader is None:
            raise ValueError("File loader is required")

        file_data = self.file_loader(
            self.owner,
            self.repo,
            path,
        )
        content = decode_file_content(file_data)

        return parse_package_json(content)