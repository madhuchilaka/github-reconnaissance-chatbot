from app.services.security_extractor import extract_security_indicators


def test_extract_credential_environment_variable():
    files = [
        {
            "path": "config/settings.py",
            "content": 'api_key = os.getenv("AWS_ACCESS_KEY_ID")',
        }
    ]

    results = extract_security_indicators(files)

    assert len(results) == 1
    assert results[0].indicator_type == "AWS_ACCESS_KEY"
    assert results[0].file_path == "config/settings.py"
    assert results[0].evidence == "AWS_ACCESS_KEY_ID"
def test_extract_security_indicators_with_no_credentials():
    files = [
        {
            "path": "src/main.py",
            "content": "print('Hello World')",
        },
        {
            "path": "README.md",
            "content": "This project uses an API.",
        },
    ]

    results = extract_security_indicators(files)

    assert results == []
def test_extract_multiple_security_indicators():
    files = [
        {
            "path": "config/aws.py",
            "content": 'key = os.getenv("AWS_ACCESS_KEY_ID")',
        },
        {
            "path": "config/backup.py",
            "content": 'backup_key = os.getenv("AWS_ACCESS_KEY_ID")',
        },
    ]

    results = extract_security_indicators(files)

    assert len(results) == 2

    assert results[0].indicator_type == "AWS_ACCESS_KEY"
    assert results[0].file_path == "config/aws.py"
    assert results[0].evidence == "AWS_ACCESS_KEY_ID"

    assert results[1].indicator_type == "AWS_ACCESS_KEY"
    assert results[1].file_path == "config/backup.py"
    assert results[1].evidence == "AWS_ACCESS_KEY_ID"
def test_extract_duplicate_indicator_in_same_file():
    files = [
        {
            "path": "config/aws.py",
            "content": (
                'key = os.getenv("AWS_ACCESS_KEY_ID")\n'
                'backup_key = os.getenv("AWS_ACCESS_KEY_ID")'
            ),
        }
    ]

    results = extract_security_indicators(files)

    assert len(results) == 1
    assert results[0].indicator_type == "AWS_ACCESS_KEY"
    assert results[0].file_path == "config/aws.py"
    assert results[0].evidence == "AWS_ACCESS_KEY_ID"
def test_extract_aws_secret_access_key():
    files = [
        {
            "path": "config/aws.py",
            "content": 'secret = os.getenv("AWS_SECRET_ACCESS_KEY")',
        }
    ]

    results = extract_security_indicators(files)

    assert len(results) == 1
    assert results[0].indicator_type == "AWS_SECRET_KEY"
    assert results[0].file_path == "config/aws.py"
    assert results[0].evidence == "AWS_SECRET_ACCESS_KEY"



def test_extract_github_personal_access_token():
    files = [
        {
            "path": "config/github.py",
            "content": 'token = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"',
        }
    ]

    results = extract_security_indicators(files)

    assert len(results) == 1
    assert results[0].indicator_type == "GITHUB_TOKEN"
    assert results[0].file_path == "config/github.py"
    assert results[0].evidence == "ghp_1234567890abcdefghijklmnopqrstuvwxyz"



def test_extract_multiple_security_indicators_from_same_file():
    files = [
        {
            "path": "config/secrets.py",
            "content": """
AWS_ACCESS_KEY_ID = "example"
AWS_SECRET_ACCESS_KEY = "example"
GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
""",
        }
    ]

    results = extract_security_indicators(files)

    assert len(results) == 3

    indicator_types = {
        result.indicator_type
        for result in results
    }

    assert indicator_types == {
        "AWS_ACCESS_KEY",
        "AWS_SECRET_KEY",
        "GITHUB_TOKEN",
    }



def test_does_not_detect_credential_name_in_documentation():
    files = [
        {
            "path": "README.md",
            "content": "Set the AWS_ACCESS_KEY_ID environment variable before running the application.",
        }
    ]

    results = extract_security_indicators(files)

    assert results == []


def test_detects_aws_access_key_assignment():
    files = [
        {
            "path": "config/aws.py",
            "content": 'AWS_ACCESS_KEY_ID = "example-access-key"',
        }
    ]

    results = extract_security_indicators(files)

    assert len(results) == 1
    assert results[0].indicator_type == "AWS_ACCESS_KEY"
    assert results[0].file_path == "config/aws.py"


def test_extract_github_fine_grained_token():
    files = [
        {
            "path": "config/github.py",
            "content": 'token = "github_pat_1234567890abcdefghijklmnopqrstuvwxyz"',
        }
    ]

    results = extract_security_indicators(files)

    assert len(results) == 1
    assert results[0].indicator_type == "GITHUB_FINE_GRAINED_TOKEN"
    assert results[0].file_path == "config/github.py"
    assert results[0].evidence == "github_pat_1234567890abcdefghijklmnopqrstuvwxyz"


def test_extract_slack_token():
    files = [
        {
            "path": "config/slack.py",
            "content": 'token = "xoxb-TEST-ONLY-NOT-A-REAL-TOKEN"',
        }
    ]

    results = extract_security_indicators(files)

    assert len(results) == 1
    assert results[0].indicator_type == "SLACK_TOKEN"
    assert results[0].file_path == "config/slack.py"
    assert results[0].evidence == "xoxb-TEST-ONLY-NOT-A-REAL-TOKEN"


def test_extract_stripe_secret_key():
    files = [
        {
            "path": "config/stripe.py",
            "content": 'stripe_key = "sk_test_1234567890abcdefghijklmnopqrstuvwxyz"',
        }
    ]

    results = extract_security_indicators(files)

    assert len(results) == 1
    assert results[0].indicator_type == "STRIPE_SECRET_KEY"
    assert results[0].file_path == "config/stripe.py"
    assert results[0].evidence == "sk_test_1234567890abcdefghijklmnopqrstuvwxyz"



def test_extract_google_api_key():
    files = [
        {
            "path": "config/google.py",
            "content": 'api_key = "AIzaSyA1234567890abcdefghijklmnopqrstuvwxyz"',
        }
    ]

    results = extract_security_indicators(files)

    assert len(results) == 1
    assert results[0].indicator_type == "GOOGLE_API_KEY"
    assert results[0].file_path == "config/google.py"
    assert results[0].evidence == "AIzaSyA1234567890abcdefghijklmnopqrstuvwxyz"


def test_extract_sendgrid_api_key():
    files = [
        {
            "path": "config/email.py",
            "content": 'api_key = "SG.abcdefghijklmnopqrstuvwxyz1234567890.ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"',
        }
    ]

    results = extract_security_indicators(files)

    assert len(results) == 1
    assert results[0].indicator_type == "SENDGRID_API_KEY"
    assert results[0].file_path == "config/email.py"
    assert results[0].evidence == (
        "SG.abcdefghijklmnopqrstuvwxyz1234567890."
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    )


def test_extract_twilio_auth_token():
    files = [
        {
            "path": "config/twilio.py",
            "content": 'auth_token = "0123456789abcdef0123456789abcdef"',
        }
    ]

    results = extract_security_indicators(files)

    assert len(results) == 1
    assert results[0].indicator_type == "TWILIO_AUTH_TOKEN"
    assert results[0].file_path == "config/twilio.py"
    assert results[0].evidence == "0123456789abcdef0123456789abcdef"