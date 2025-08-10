from functools import lru_cache

from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Either provide full DATABASE_URL or component vars (preferred minimal: components only)
    DATABASE_URL: AnyUrl | None = None  # type: ignore
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "lekhamudra"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    ENV: str = "dev"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    LOG_LEVEL: str = "INFO"
    ENABLE_REQUEST_LOGGING: bool = True

    def assembled_database_url(self) -> str:
        if self.DATABASE_URL:
            return str(self.DATABASE_URL)
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Pydantic v2 settings config (replaces deprecated inner Config)
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache(maxsize=1)
def get_settings() -> Settings:  # cached single Settings instance
    return Settings()
