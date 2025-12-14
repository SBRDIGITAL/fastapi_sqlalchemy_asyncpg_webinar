from fastapi import APIRouter

from app.api.v1.models.response.healthcheck import HealthCheckResponseModel

# from enum import Enum


# class ExampleEnum(Enum):
#     EN_1 = 'THIS_IS_ENUM_1'
#     EN_2 = 'THIS_IS_ENUM_2'

# Если используете енамы, то их надо распаковать с помощью оператора "*"
# router = APIRouter(prefix='/lifecheck', tags=[*ExampleEnum])


router = APIRouter(prefix='/healthcheck', tags=['healthcheck', 'v1'])


@router.get(path='/', status_code=200, response_model=HealthCheckResponseModel)
async def get_healthcheck():
    """
    ## Ендпоинт проверки работоспособности `API`.

    ### Returns:
        HealthCheckResponseModel: Модель для ответа от `'/v1/healthcheck'`
    """    
    return HealthCheckResponseModel()