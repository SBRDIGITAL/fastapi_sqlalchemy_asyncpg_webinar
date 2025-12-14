"""Базовые исключения для API."""

from fastapi import HTTPException

from .statuses import NOT_FOUND



class BaseAPIException(HTTPException):
    """
    ## Базовое исключение для API.

    Используется для создания пользовательских исключений с заданным статусом и описанием.

    ### Inherits:
        HTTPException: Исключение FastAPI для HTTP-ответов.
    """    
    def __init__(self, status_code: int, detail: str):
        """
        ## Инициализация базового исключения.

        ### Args:
            status_code (int): HTTP-статус код.
            detail (str): Описание ошибки.
        """        
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(BaseAPIException):
    """
    ## Исключение: Ресурс не найден.

    Используется для случаев, когда запрашиваемый ресурс отсутствует.

    ### Inherits:
        BaseAPIException: Базовое исключение для API.
    """    
    def __init__(self, resource_name: str):
        """
        ## Инициализация исключения.

        Формирует сообщение об ошибке с указанием имени ресурса.

        ### Args:
            resource_name (str): Название ресурса.
        """        
        detail = f"{resource_name} не найден."
        super().__init__(status_code=NOT_FOUND, detail=detail)