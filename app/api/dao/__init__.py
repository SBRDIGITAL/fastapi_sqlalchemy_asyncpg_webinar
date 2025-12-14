"""Пакет DAO для работы с данными в API."""

from .base import BaseDAO
from .user import UserDAO, user_dao

__all__ = [
	'BaseDAO',
	'UserDAO',
	'user_dao',
]
