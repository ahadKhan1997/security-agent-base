from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: str = "mock_local_secret_key_12345"
    database_url: str = "postgresql://user:password@localhost:5432/cyber_db"
    groq_api_key: str = "mock_gsk_cloud_token_placeholder"
    target_model: str = "openai/gpt-oss-120b"
    max_concurrency: int = 2

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_file_required = False

settings = Settings()