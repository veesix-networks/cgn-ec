from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    CORS_ORIGINS: list[str] = [
        "http://localhost:8000",
    ]
    CORS_HEADERS: list[str] = ["*"]

    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DEFAULT_LOOKBACK_HOURS: int = 3

    API_KEY_HEADER: str = "x-api-key"
    API_KEYS: list[str] = ["default-change-me"]


settings = Settings()
