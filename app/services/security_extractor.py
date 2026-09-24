import re

from app.models.security_indicator import SecurityIndicator


CREDENTIAL_ENV_PATTERNS = {
    "AWS_ACCESS_KEY": re.compile(
        r'(?P<indicator>\bAWS_ACCESS_KEY_ID\b)'
        r'(?:\s*(?:=|:)\s*[\'"][^\'"]+[\'"]|'
        r'\s*["\']?\s*\))'
    ),
    "AWS_SECRET_KEY": re.compile(
        r'(?P<indicator>\bAWS_SECRET_ACCESS_KEY\b)'
        r'(?:\s*(?:=|:)\s*[\'"][^\'"]+[\'"]|'
        r'\s*["\']?\s*\))'
    ),
}

GITHUB_FINE_GRAINED_TOKEN_PATTERN = re.compile(
    r"\bgithub_pat_[A-Za-z0-9_]{22,255}\b"
)

GITHUB_TOKEN_PATTERN = re.compile(
    r"\bghp_[A-Za-z0-9]{36}\b"
)

SLACK_TOKEN_PATTERN = re.compile(
    r"\bxox[baprs]-[A-Za-z0-9-]+\b"
)

STRIPE_SECRET_KEY_PATTERN = re.compile(
    r"\bsk_(?:live|test)_[A-Za-z0-9]+\b"
)

GOOGLE_API_KEY_PATTERN = re.compile(
    r"\bAIza[A-Za-z0-9_-]{39}\b"
)

SENDGRID_API_KEY_PATTERN = re.compile(
    r"\bSG\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"
)

TWILIO_AUTH_TOKEN_PATTERN = re.compile(
    r"\b[A-Fa-f0-9]{32}\b"
)




def extract_security_indicators(
    files: list[dict],
) -> list[SecurityIndicator]:
    results: list[SecurityIndicator] = []

    for file_data in files:
        path = file_data["path"]
        content = file_data.get("content", "")

        for indicator_type, pattern in CREDENTIAL_ENV_PATTERNS.items():
            match = pattern.search(content)

            if match:
                results.append(
                    SecurityIndicator(
                        indicator_type=indicator_type,
                        file_path=path,
                        evidence=match.group("indicator"),
                    )
                )

        github_match = GITHUB_TOKEN_PATTERN.search(content)

        github_fine_grained_match = GITHUB_FINE_GRAINED_TOKEN_PATTERN.search(content)

        slack_match = SLACK_TOKEN_PATTERN.search(content)

        stripe_match = STRIPE_SECRET_KEY_PATTERN.search(content)


        google_match = GOOGLE_API_KEY_PATTERN.search(content)

        sendgrid_match = SENDGRID_API_KEY_PATTERN.search(content)

        twilio_match = TWILIO_AUTH_TOKEN_PATTERN.search(content)

        if twilio_match:
            results.append(
                SecurityIndicator(
                    indicator_type="TWILIO_AUTH_TOKEN",
                    file_path=path,
                    evidence=twilio_match.group(0),
                )
            )

        if sendgrid_match:
            results.append(
                SecurityIndicator(
                    indicator_type="SENDGRID_API_KEY",
                    file_path=path,
                    evidence=sendgrid_match.group(0),
                )
            )

        if google_match:
            results.append(
                SecurityIndicator(
                    indicator_type="GOOGLE_API_KEY",
                    file_path=path,
                    evidence=google_match.group(0),
                )
            )

        if stripe_match:
            results.append(
                SecurityIndicator(
                    indicator_type="STRIPE_SECRET_KEY",
                    file_path=path,
                    evidence=stripe_match.group(0),
                )
            )

        if slack_match:
            results.append(
                SecurityIndicator(
                    indicator_type="SLACK_TOKEN",
                    file_path=path,
                    evidence=slack_match.group(0),
                )
            )

        if github_fine_grained_match:
            results.append(
                SecurityIndicator(
                    indicator_type="GITHUB_FINE_GRAINED_TOKEN",
                    file_path=path,
                    evidence=github_fine_grained_match.group(0),
                )
            )



        if github_match:
            results.append(
                SecurityIndicator(
                    indicator_type="GITHUB_TOKEN",
                    file_path=path,
                    evidence=github_match.group(0),
                )
            )

    return results