from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "OmniAgent"
    app_version: str = "0.1.0"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
