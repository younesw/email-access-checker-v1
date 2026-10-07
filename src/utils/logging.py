from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "email-access-checker"
    env_file: str = ".env"
    secret_key: str = "change-me-super-secret-key" 
    db_url: str = "sqlite:///./data/email_access_checker.db"
    log_level: str = "INFO"
    max_workers: int = 8
    rate_limit_per_minute: int = 60
    request_timeout_seconds: float = 5.0
    tls_required: bool = True
    allow_custom_imap: bool = True
    allowed_providers: str = "gmail,outlook,yahoo,protonmail,custom"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
