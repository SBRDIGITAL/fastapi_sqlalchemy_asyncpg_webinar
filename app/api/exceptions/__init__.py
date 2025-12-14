"""Пакет пользовательских исключений для API."""

from .base import BaseAPIException, NotFoundException
from .user import UserNotFoundException

__all__ = [
    'BaseAPIException',
    'NotFoundException',
    'UserNotFoundException',
]