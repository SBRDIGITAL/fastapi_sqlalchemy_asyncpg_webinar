"""Пакет схем данных для API."""

from .user import NewUser, ExistsUser

__all__ = [
    "NewUser",
    "ExistsUser",
]