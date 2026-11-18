"""
[CORE] config.py - Configuración central vía .env (pydantic-settings).
Ubicación: app/core/config.py
Responsabilidad: Capa CORE - Lee variables de entorno (DATABASE_URL, SECRET_KEY, MOCK_MODE, Football API) y expone singleton `settings`. No toca DB.
Usa: pydantic_settings.BaseSettings, .env
No hace: No crea engine ni valida contra BD, solo carga config en memoria.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_ENV: str = "dev"
    SECRET_KEY: str = "change-me-32chars-minimum-secret-key-please"
    JWT_EXPIRE_HOURS: int = 24

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/quiniela"

    # Football API
    FOOTBALL_API_KEY: str | None = None
    FOOTBALL_API_PROVIDER: str = "api-football"
    FOOTBALL_API_BASE: str = "https://v3.football.api-sports.io"
    MOCK_MODE: bool = True

    # Scheduler
    FIXTURES_CRON_HOUR: int = 6
    RESULTS_POLL_SECONDS: int = 600

    # Optional
    REDIS_URL: str | None = None


settings = Settings()
