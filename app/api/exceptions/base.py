from fastapi import HTTPException
from .statuses import NOT_FOUND


class BaseAPIException(HTTPException):
    """
    ## _summary_

    Args:
        HTTPException (_type_): _description_
    """    
    def __init__(self, status_code: int, detail: str):
        """
        ## _summary_

        Args:
            status_code (int): _description_
            detail (str): _description_
        """        
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(BaseAPIException):
    """
    ## _summary_

    Args:
        BaseAPIException (_type_): _description_
    """    
    def __init__(self, resource_name: str):
        """
        ## _summary_

        Args:
            resource_name (str): _description_
        """        
        detail = f"{resource_name} не найден."
        super().__init__(status_code=NOT_FOUND, detail=detail)