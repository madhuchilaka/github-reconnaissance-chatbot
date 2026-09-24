from app.models.technology_indicator import TechnologyIndicator
from app.services.technology_extractor import (
    detect_cpp,
    detect_docker,
    detect_go,
    detect_java,
    detect_javascript,
    detect_kotlin,
    detect_nodejs,
    detect_php,
    detect_python,
    detect_ruby,
    detect_rust,
    detect_swift,
    detect_typescript,
    detect_react,
    detect_express,
    
)



def test_technology_indicator():
    indicator = TechnologyIndicator(
        name="Python",
        category="language",
        evidence=["app/main.py", "requirements.txt"],
    )

    assert indicator.name == "Python"
    assert indicator.category == "language"
    assert indicator.evidence == [
        "app/main.py",
        "requirements.txt",
    ]


def test_detect_python():
    result = detect_python(
        [
            {
                "name": "main.py",
                "path": "app/main.py",
                "type": "file",
            },
            {
                "name": "utils.py",
                "path": "app/utils.py",
                "type": "file",
            },
        ]
    )

    assert result == TechnologyIndicator(
        name="Python",
        category="language",
        evidence=[
            "app/main.py",
            "app/utils.py",
        ],
    )


def test_detect_python_returns_none_when_absent():
    result = detect_python(
        [
            {
                "name": "app.js",
                "path": "app/app.js",
                "type": "file",
            }
        ]
    )

    assert result is None


def test_detect_javascript():
    result = detect_javascript(
        [
            {
                "name": "app.js",
                "path": "src/app.js",
                "type": "file",
            },
            {
                "name": "App.jsx",
                "path": "src/App.jsx",
                "type": "file",
            },
        ]
    )

    assert result == TechnologyIndicator(
        name="JavaScript",
        category="language",
        evidence=[
            "src/app.js",
            "src/App.jsx",
        ],
    )


def test_detect_javascript_returns_none_when_absent():
    result = detect_javascript(
        [
            {
                "name": "main.py",
                "path": "app/main.py",
                "type": "file",
            }
        ]
    )

    assert result is None



def test_detect_typescript():
    result = detect_typescript(
        [
            {
                "name": "main.ts",
                "path": "src/main.ts",
                "type": "file",
            },
            {
                "name": "App.tsx",
                "path": "src/App.tsx",
                "type": "file",
            },
        ]
    )

    assert result == TechnologyIndicator(
        name="TypeScript",
        category="language",
        evidence=[
            "src/main.ts",
            "src/App.tsx",
        ],
    )


def test_detect_typescript_returns_none_when_absent():
    result = detect_typescript(
        [
            {
                "name": "main.py",
                "path": "app/main.py",
                "type": "file",
            }
        ]
    )

    assert result is None



def test_detect_java():
    result = detect_java(
        [
            {
                "name": "Main.java",
                "path": "src/Main.java",
                "type": "file",
            }
        ]
    )

    assert result == TechnologyIndicator(
        name="Java",
        category="language",
        evidence=["src/Main.java"],
    )


def test_detect_java_returns_none_when_absent():
    result = detect_java(
        [
            {
                "name": "main.py",
                "path": "app/main.py",
                "type": "file",
            }
        ]
    )

    assert result is None



def test_detect_go():
    result = detect_go(
        [
            {
                "name": "main.go",
                "path": "cmd/main.go",
                "type": "file",
            }
        ]
    )

    assert result == TechnologyIndicator(
        name="Go",
        category="language",
        evidence=["cmd/main.go"],
    )


def test_detect_go_returns_none_when_absent():
    result = detect_go(
        [
            {
                "name": "main.py",
                "path": "app/main.py",
                "type": "file",
            }
        ]
    )

    assert result is None


def test_detect_rust():
    result = detect_rust(
        [
            {
                "name": "main.rs",
                "path": "src/main.rs",
                "type": "file",
            }
        ]
    )

    assert result == TechnologyIndicator(
        name="Rust",
        category="language",
        evidence=["src/main.rs"],
    )


def test_detect_rust_returns_none_when_absent():
    result = detect_rust(
        [
            {
                "name": "main.py",
                "path": "app/main.py",
                "type": "file",
            }
        ]
    )

    assert result is None


def test_detect_cpp():
    result = detect_cpp(
        [
            {
                "name": "main.cpp",
                "path": "src/main.cpp",
                "type": "file",
            },
            {
                "name": "utils.h",
                "path": "include/utils.h",
                "type": "file",
            },
        ]
    )

    assert result == TechnologyIndicator(
        name="C/C++",
        category="language",
        evidence=[
            "src/main.cpp",
            "include/utils.h",
        ],
    )


def test_detect_cpp_returns_none_when_absent():
    result = detect_cpp(
        [
            {
                "name": "main.py",
                "path": "app/main.py",
                "type": "file",
            }
        ]
    )

    assert result is None


def test_detect_php():
    result = detect_php(
        [
            {
                "name": "index.php",
                "path": "public/index.php",
                "type": "file",
            }
        ]
    )

    assert result == TechnologyIndicator(
        name="PHP",
        category="language",
        evidence=["public/index.php"],
    )


def test_detect_php_returns_none_when_absent():
    result = detect_php(
        [
            {
                "name": "main.py",
                "path": "app/main.py",
                "type": "file",
            }
        ]
    )

    assert result is None


def test_detect_ruby():
    result = detect_ruby(
        [
            {
                "name": "app.rb",
                "path": "lib/app.rb",
                "type": "file",
            }
        ]
    )

    assert result == TechnologyIndicator(
        name="Ruby",
        category="language",
        evidence=["lib/app.rb"],
    )


def test_detect_ruby_returns_none_when_absent():
    result = detect_ruby(
        [
            {
                "name": "main.py",
                "path": "app/main.py",
                "type": "file",
            }
        ]
    )

    assert result is None


def test_detect_swift():
    result = detect_swift(
        [
            {
                "name": "App.swift",
                "path": "Sources/App.swift",
                "type": "file",
            }
        ]
    )

    assert result == TechnologyIndicator(
        name="Swift",
        category="language",
        evidence=["Sources/App.swift"],
    )


def test_detect_swift_returns_none_when_absent():
    result = detect_swift(
        [
            {
                "name": "main.py",
                "path": "app/main.py",
                "type": "file",
            }
        ]
    )

    assert result is None


def test_detect_kotlin():
    result = detect_kotlin(
        [
            {
                "name": "Main.kt",
                "path": "src/Main.kt",
                "type": "file",
            }
        ]
    )

    assert result == TechnologyIndicator(
        name="Kotlin",
        category="language",
        evidence=["src/Main.kt"],
    )


def test_detect_kotlin_returns_none_when_absent():
    result = detect_kotlin(
        [
            {
                "name": "main.py",
                "path": "app/main.py",
                "type": "file",
            }
        ]
    )

    assert result is None


def test_detect_docker():
    result = detect_docker(
        [
            {
                "name": "Dockerfile",
                "path": "Dockerfile",
                "type": "file",
            }
        ]
    )

    assert result == TechnologyIndicator(
        name="Docker",
        category="container",
        evidence=["Dockerfile"],
    )


def test_detect_docker_returns_none_when_absent():
    result = detect_docker(
        [
            {
                "name": "main.py",
                "path": "app/main.py",
                "type": "file",
            }
        ]
    )

    assert result is None


def test_detect_nodejs():
    result = detect_nodejs(
        [
            {
                "name": "package.json",
                "path": "package.json",
                "type": "file",
            }
        ]
    )

    assert result == TechnologyIndicator(
        name="Node.js",
        category="runtime",
        evidence=["package.json"],
    )


def test_detect_nodejs_returns_none_when_absent():
    result = detect_nodejs(
        [
            {
                "name": "main.py",
                "path": "app/main.py",
                "type": "file",
            }
        ]
    )

    assert result is None


def test_detect_react_from_dependencies():
    result = detect_react(
        "package.json",
        {
            "dependencies": {
                "react": "^19.0.0",
                "react-dom": "^19.0.0",
            }
        },
    )

    assert result == TechnologyIndicator(
        name="React",
        category="framework",
        evidence=["package.json"],
    )


def test_detect_react_from_dev_dependencies():
    result = detect_react(
        "package.json",
        {
            "devDependencies": {
                "react": "^19.0.0",
            }
        },
    )

    assert result == TechnologyIndicator(
        name="React",
        category="framework",
        evidence=["package.json"],
    )


def test_detect_react_returns_none_when_absent():
    result = detect_react(
        "package.json",
        {
            "dependencies": {
                "express": "^5.0.0",
            }
        },
    )

    assert result is None


def test_detect_express_from_dependencies():
    result = detect_express(
        "package.json",
        {
            "dependencies": {
                "express": "^5.0.0",
            }
        },
    )

    assert result == TechnologyIndicator(
        name="Express",
        category="framework",
        evidence=["package.json"],
    )


def test_detect_express_from_dev_dependencies():
    result = detect_express(
        "package.json",
        {
            "devDependencies": {
                "express": "^5.0.0",
            }
        },
    )

    assert result == TechnologyIndicator(
        name="Express",
        category="framework",
        evidence=["package.json"],
    )


def test_detect_express_returns_none_when_absent():
    result = detect_express(
        "package.json",
        {
            "dependencies": {
                "react": "^19.0.0",
            }
        },
    )

    assert result is None