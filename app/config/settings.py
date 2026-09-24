import os

from dotenv import load_dotenv


load_dotenv()


GITHUB_API_BASE_URL = os.getenv(
    "GITHUB_API_BASE_URL",
    "https://api.github.com",
)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GITHUB_API_TIMEOUT = float(
    os.getenv("GITHUB_API_TIMEOUT", "30.0")
)

GITHUB_MAX_RETRIES = int(
    os.getenv("GITHUB_MAX_RETRIES", "3")
)

GITHUB_RETRY_BACKOFF = float(
    os.getenv("GITHUB_RETRY_BACKOFF", "1.0")
)


DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "data/security_findings.db",
)