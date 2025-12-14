from functools import lru_cache


from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    """
    ## Читает переменные окружения из `.env` файла в кодировке `UTF-8`.
    """
    # FastAPI
    api_host: str = Field("localhost", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")

    # PostgreSQL
    db_name: str = Field("postgrocker_db", env="POSTGRES_DB")
    db_user: str = Field("postgrocker_user", env="POSTGRES_USER")
    db_password: str = Field("postgrocker_password", env="POSTGRES_PASSWORD")
    db_host: str = Field("localhost", env="POSTGRES_HOST")
    db_port: int = Field(5495, env="POSTGRES_PORT")

    # SQLAlchemy
    db_echo: bool = Field(True, env="DB_ECHO")
    db_pool_size: int = Field(10, env="DB_POOL_SIZE")
    db_max_overflow: int = Field(20, env="DB_MAX_OVERFLOW")

    # Дополнительные настройки
    env: str = Field("development", env="ENV")

    @property
    def DATABASE_URL_asyncpg(self):
        return (
            f"postgresql+asyncpg://{self.db_user}:"
            f"{self.db_password}@{self.db_host}:"
            f"{self.db_port}/{self.db_name}"
        )
    

    # pydantic-settings configuration: указываем .env и кодировку UTF-8
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='UTF-8',
        populate_by_name=True,
        case_sensitive=False,  # принимаем переменные окружения независимо от регистра
        extra="ignore",  # игнорируем неожиданные ключи вместо ошибки
        # https://docs.pydantic.dev/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource.prepare_field_value
    )


@lru_cache
def get_settings() -> Settings:
    """
    ## Возвращает кешированный экземпляр `Settings`.

    lru_cache обеспечивает, что настройки будут прочитаны один раз при
    первом вызове и потом переиспользоваться (удобно для FastAPI зависимостей).
    """
    return Settings()


env_config = get_settings()


# Экспортируемый интерфейс модуля
__all__ = [
    "env_config",
]