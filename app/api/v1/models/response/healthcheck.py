# Плохо
# from ..base import BaseResponseModel
# Хорошо (Явное лучше неявного)
from app.api.v1.models.base import BaseResponseModel



class HealthCheckResponseModel(BaseResponseModel):
    """
    ## Модель для ответа от `'/v1/healthcheck'`.

    Args:
        BaseModel (pydantic.BaseModel): ...
    
    Attributes:
        status_code (int): Статус код..
        description (str): Описание результата..
    """    
    description: str = 'API работает'