from openai import OpenAI

from app.config.settings import OPENAI_API_KEY


class AIClient:
    def __init__(self) -> None:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured")

        self.client = OpenAI(api_key=OPENAI_API_KEY)