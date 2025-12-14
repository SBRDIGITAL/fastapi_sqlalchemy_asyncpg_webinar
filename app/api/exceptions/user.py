from .base import NotFoundException


class UserNotFoundException(NotFoundException):
    """
    ## _summary_

    Args:
        NotFoundException (_type_): _description_
    """    
    def __init__(self, user_id: int):
        """
        ## _summary_

        `НЕ ДОПОЛНЯТЬ "не найден"`!

        Args:
            user_id (int): _description_
        """        
        detail = f"Пользователь с идентификатором {user_id}."
        super().__init__(resource_name=detail)