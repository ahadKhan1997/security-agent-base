from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    api_key: str = "mock_local_secret_key_12345"
    database_url: str = "postgresql://user:password@localhost:5432/cyber_db"
    groq_api_key: str = "mock_gsk_cloud_token_placeholder"
    target_model: str = "openai/gpt-oss-120b"
    max_concurrency: int = 2

    @property
    def adjusted_db_url(self) -> str:
        """Dynamically adjusts the DB hostname based on execution environment context."""
        url = self.database_url
        # If running locally on Windows outside Docker, swap 'db' out for 'localhost'
        if not os.path.exists("/.dockerenv") and "@db:" in url:
            url = url.replace("@db:", "@localhost:")
        return url

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_file_required = False

settings = Settings()