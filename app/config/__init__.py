"""Пакет конфигурации приложения."""

from .config_reader import env_config
from .constants import PROD_ENV, DEV_ENV


__all__ = [
    "env_config",
    "PROD_ENV",
    "DEV_ENV",
]