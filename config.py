from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: str
    database_url: str
    max_concurrency: int = 2
    groq_api_key: str
    target_model: str = "openai/gpt-oss-120b"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()