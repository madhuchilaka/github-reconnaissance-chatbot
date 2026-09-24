from app.services.security_analysis_service import analyze_security


def test_analyze_security_builds_redacted_findings():
    files = [
        {
            "path": "config/github.py",
            "content": "token = 'ghp_1234567890abcdefghijklmnopqrstuvwxyz'",
        },
        {
            "path": "config/aws.py",
            "content": "AWS_ACCESS_KEY_ID = 'AKIA1234567890EXAMPLE'",
        },
    ]

    findings = analyze_security(files)

    assert len(findings) == 2

    assert findings[0].indicator_type == "GITHUB_TOKEN"
    assert findings[0].file_path == "config/github.py"
    assert findings[0].evidence == "ghp_********************"

    assert findings[1].indicator_type == "AWS_ACCESS_KEY"
    assert findings[1].file_path == "config/aws.py"
    assert findings[1].evidence == "AWS_********************"


def test_analyze_security_with_no_indicators():
    files = [
        {
            "path": "README.md",
            "content": "This project uses environment variables for configuration.",
        }
    ]

    findings = analyze_security(files)

    assert findings == []