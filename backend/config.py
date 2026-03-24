
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Authentication settings
    secret_key: str = "secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Database settings
    database_url: str = "sqlite:///./sql_app.db"

    # CORS settings
    cors_origins: List[str] = ["http://localhost:3000"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    # Application settings
    app_name: str = "Lekhamudra Backend"
    app_version: str = "0.1.0"
    debug: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()