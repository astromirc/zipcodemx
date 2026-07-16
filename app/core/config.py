from typing import Annotated, Literal

from pydantic import BeforeValidator, EmailStr, Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_allowed_cors_origins(v: str | list[str] | None) -> list[str]:
    """Parsea y limpia orígenes CORS desde una lista o cadena separada por comas."""
    if isinstance(v, list):
        return v
    if v and isinstance(v, str):
        return [origin.strip() for origin in v.split(",")]

    return []


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        case_sensitive=True,
        extra="forbid",
        frozen=True,
    )

    # App
    NAME: str
    DESCRIPTION: str
    VERSION: str = Field(pattern=r"^\d+\.\d+\.\d+$")

    # Security
    SECRET_KEY: str = Field(min_length=32)
    ALLOWED_CORS_ORIGINS: Annotated[
        list[str] | str,
        BeforeValidator(_parse_allowed_cors_origins),
    ] = []
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # PostgreSQL
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # Email SMTP
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: EmailStr

    # Frontend
    FRONTEND_URL: str

    # Entorno (Dependiendo de la configuración del contenedor)
    ENVIRONMENT: Literal["local", "production"] = "local"

    @property
    def is_debug(self) -> bool:
        """
        Determina si la aplicación está en modo debug basándose en el entorno.
        Se realiza de manera automática.
        """
        return self.ENVIRONMENT == "local"

    @computed_field
    @property
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = AppSettings()  # type: ignore
