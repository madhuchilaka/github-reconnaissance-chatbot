from app.models.technology_indicator import TechnologyIndicator


def detect_python(files: list[dict]) -> TechnologyIndicator | None:
    evidence = [
        file_data["path"]
        for file_data in files
        if file_data.get("name", "").lower().endswith(".py")
    ]

    if not evidence:
        return None

    return TechnologyIndicator(
        name="Python",
        category="language",
        evidence=evidence,
    )

def detect_javascript(files: list[dict]) -> TechnologyIndicator | None:
    evidence = [
        file_data["path"]
        for file_data in files
        if file_data.get("name", "").lower().endswith((".js", ".jsx"))
    ]

    if not evidence:
        return None

    return TechnologyIndicator(
        name="JavaScript",
        category="language",
        evidence=evidence,
    )



def detect_typescript(files: list[dict]) -> TechnologyIndicator | None:
    evidence = [
        file_data["path"]
        for file_data in files
        if file_data.get("name", "").lower().endswith((".ts", ".tsx"))
    ]

    if not evidence:
        return None

    return TechnologyIndicator(
        name="TypeScript",
        category="language",
        evidence=evidence,
    )


def detect_java(files: list[dict]) -> TechnologyIndicator | None:
    evidence = [
        file_data["path"]
        for file_data in files
        if file_data.get("name", "").lower().endswith(".java")
    ]

    if not evidence:
        return None

    return TechnologyIndicator(
        name="Java",
        category="language",
        evidence=evidence,
    )


def detect_go(files: list[dict]) -> TechnologyIndicator | None:
    evidence = [
        file_data["path"]
        for file_data in files
        if file_data.get("name", "").lower().endswith(".go")
    ]

    if not evidence:
        return None

    return TechnologyIndicator(
        name="Go",
        category="language",
        evidence=evidence,
    )


def detect_rust(files: list[dict]) -> TechnologyIndicator | None:
    evidence = [
        file_data["path"]
        for file_data in files
        if file_data.get("name", "").lower().endswith(".rs")
    ]

    if not evidence:
        return None

    return TechnologyIndicator(
        name="Rust",
        category="language",
        evidence=evidence,
    )


def detect_cpp(files: list[dict]) -> TechnologyIndicator | None:
    evidence = [
        file_data["path"]
        for file_data in files
        if file_data.get("name", "").lower().endswith(
            (".c", ".cc", ".cpp", ".cxx", ".h", ".hpp")
        )
    ]

    if not evidence:
        return None

    return TechnologyIndicator(
        name="C/C++",
        category="language",
        evidence=evidence,
    )


def detect_php(files: list[dict]) -> TechnologyIndicator | None:
    evidence = [
        file_data["path"]
        for file_data in files
        if file_data.get("name", "").lower().endswith(".php")
    ]

    if not evidence:
        return None

    return TechnologyIndicator(
        name="PHP",
        category="language",
        evidence=evidence,
    )


def detect_ruby(files: list[dict]) -> TechnologyIndicator | None:
    evidence = [
        file_data["path"]
        for file_data in files
        if file_data.get("name", "").lower().endswith(".rb")
    ]

    if not evidence:
        return None

    return TechnologyIndicator(
        name="Ruby",
        category="language",
        evidence=evidence,
    )


def detect_swift(files: list[dict]) -> TechnologyIndicator | None:
    evidence = [
        file_data["path"]
        for file_data in files
        if file_data.get("name", "").lower().endswith(".swift")
    ]

    if not evidence:
        return None

    return TechnologyIndicator(
        name="Swift",
        category="language",
        evidence=evidence,
    )


def detect_kotlin(files: list[dict]) -> TechnologyIndicator | None:
    evidence = [
        file_data["path"]
        for file_data in files
        if file_data.get("name", "").lower().endswith(".kt")
    ]

    if not evidence:
        return None

    return TechnologyIndicator(
        name="Kotlin",
        category="language",
        evidence=evidence,
    )


def detect_docker(files: list[dict]) -> TechnologyIndicator | None:
    evidence = [
        file_data["path"]
        for file_data in files
        if file_data.get("name", "").lower() == "dockerfile"
    ]

    if not evidence:
        return None

    return TechnologyIndicator(
        name="Docker",
        category="container",
        evidence=evidence,
    )



def detect_nodejs(files: list[dict]) -> TechnologyIndicator | None:
    evidence = [
        file_data["path"]
        for file_data in files
        if file_data.get("name", "").lower() == "package.json"
    ]

    if not evidence:
        return None

    return TechnologyIndicator(
        name="Node.js",
        category="runtime",
        evidence=evidence,
    )



def detect_react(
    package_path: str,
    package_data: dict,
) -> TechnologyIndicator | None:
    dependencies = package_data.get("dependencies", {})
    dev_dependencies = package_data.get("devDependencies", {})

    if "react" not in dependencies and "react" not in dev_dependencies:
        return None

    return TechnologyIndicator(
        name="React",
        category="framework",
        evidence=[package_path],
    )


def detect_express(
    package_path: str,
    package_data: dict,
) -> TechnologyIndicator | None:
    dependencies = package_data.get("dependencies", {})
    dev_dependencies = package_data.get("devDependencies", {})

    if "express" not in dependencies and "express" not in dev_dependencies:
        return None

    return TechnologyIndicator(
        name="Express",
        category="framework",
        evidence=[package_path],
    )