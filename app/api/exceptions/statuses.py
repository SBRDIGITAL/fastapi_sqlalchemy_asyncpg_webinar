"""HTTP-статусы для пользовательских исключений."""

from fastapi import status


NOT_FOUND = status.HTTP_404_NOT_FOUND
"""
    ## NOT_FOUND

    HTTP-статус для случаев, когда запрашиваемый ресурс отсутствует.
"""