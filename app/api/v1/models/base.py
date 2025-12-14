from pydantic import BaseModel, Field

# В Visual Studio Code создать шаблон для документации
# ctrl + Lshift + F2
# https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring


class BaseResponseModel(BaseModel):
    """
    ## Базовая модель для ответа клиенту от API

    Args:
        BaseModel (pydantic.BaseModel): ...
    
    Attributes:
        status_code (int): Статус код..
        description (str): Описание результата..
    """    
    status_code: int = Field(
        default=200,
        description='Статус код говорящий об успешности или неуспешности обращения к ендпоинту'
    )
    description: str = Field(
        default='Запрос выполнен',
        description='Описание результата обращения к ендпоинту'
    )