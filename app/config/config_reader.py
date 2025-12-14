"""Чтение и управление конфигурацией приложения."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict



BASE_DIR = Path(__file__).resolve().parent.parent.parent



class Settings(BaseSettings):
    """
    ## Конфигурация приложения.

    Читает переменные окружения из `.env` файла и предоставляет доступ к настройкам.

    ### Attributes:
        api_host (str): Хост для `API`.
        api_port (int): Порт для `API`.
        db_name (str): Имя базы данных `PostgreSQL`.
        db_user (str): Пользователь базы данных `PostgreSQL`.
        db_password (str): Пароль для базы данных `PostgreSQL`.
        db_host (str): Хост базы данных `PostgreSQL`.
        db_port (int): Порт базы данных `PostgreSQL`.
        db_echo (bool): Логирование `SQL`-запросов.
        db_pool_size (int): Размер пула соединений.
        db_max_overflow (int): Максимальное количество дополнительных соединений.
        env (str): Текущая среда (`production`/`development`).
    """

    # FastAPI
    api_host: str = Field("localhost", validation_alias="API_HOST")
    api_port: int = Field(8000, validation_alias="API_PORT")

    # PostgreSQL
    db_name: str = Field("postgrocker_db", validation_alias="POSTGRES_DB")
    db_user: str = Field("postgrocker_user", validation_alias="POSTGRES_USER")
    db_password: str = Field("postgrocker_password", validation_alias="POSTGRES_PASSWORD")
    db_host: str = Field("localhost", validation_alias="POSTGRES_HOST")
    db_port: int = Field(5432, validation_alias="POSTGRES_PORT")

    # SQLAlchemy
    db_echo: bool = Field(True, validation_alias="DB_ECHO")
    db_pool_size: int = Field(10, validation_alias="DB_POOL_SIZE")
    db_max_overflow: int = Field(20, validation_alias="DB_MAX_OVERFLOW")

    # Дополнительные настройки
    env: str = Field("development", validation_alias="ENV")

    @property
    def DATABASE_URL_asyncpg(self):
        return (
            f"postgresql+asyncpg://{self.db_user}:"
            f"{self.db_password}@{self.db_host}:"
            f"{self.db_port}/{self.db_name}"
        )
    

    # pydantic-settings configuration: указываем .env и кодировку UTF-8
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='UTF-8',
        populate_by_name=True,
        case_sensitive=False,  # принимаем переменные окружения независимо от регистра
        extra="ignore",  # игнорируем неожиданные ключи вместо ошибки
        # https://docs.pydantic.dev/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource.prepare_field_value
    )


@lru_cache
def get_settings() -> Settings:
    """
    ## Получение настроек.

    Возвращает кэшированный экземпляр настроек приложения.

    ### Returns:
        Settings: Экземпляр настроек.
    """
    return Settings()


env_config = get_settings()


# Экспортируемый интерфейс модуля
__all__ = [
    "env_config",
]