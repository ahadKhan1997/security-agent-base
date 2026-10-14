from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    api_key: str = "mock_local_secret_key_12345"
    database_url: str = "postgresql://user:password@localhost:5432/cyber_db"
    groq_api_key: str = "mock_gsk_cloud_token_placeholder"
    target_model: str = "qwen/qwen3.8-27b"
    max_concurrency: int = 2

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def clean_groq_api_key(self) -> str:
        """Strips accidental quotes and whitespace from environment variable."""
        return self.groq_api_key.strip('"').strip("'").strip()

settings = Settings()