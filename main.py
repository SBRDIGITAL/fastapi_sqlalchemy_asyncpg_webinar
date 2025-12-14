# from app.config.config_reader import env_config

from typing import Union

from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from app.config.config_reader import env_config
from app.modules.logging.app_logger import get_app_logger
from app.config.constants import DEV_ENV, PROD_ENV

from app.api.v1.routes.healthcheck import router as healthcheck_router



logger = get_app_logger(__name__)



class FastAPIapp:
    """
    ## Класс для инициализации и настройки `FastAPI` приложения.

    Управляет созданием экземпляра `FastAPI`, регистрацией роутеров и 
    жизненным циклом приложения.

    Attributes:
        app (FastAPI): Экземпляр приложения `FastAPI`.
        app_routers (dict[str, list[APIRouter]]): Словарь роутеров, где ключ - префикс,
            а значение - список роутеров для этого префикса.
    """
    def __init__(self):
        """
        ## Инициализирует экземпляр класса.
        """
        self.app = self._create_app()
        self.app_routers: dict[str, list[APIRouter]] = {
            '/v1': [
                healthcheck_router,
                # роутер_который_не_нужен_но_удалять_не_хочу просто закомментить
                # другие роутеры..
            ]
        }
        self.__post_init()
    
    def __post_init(self):
        """ ## Выполняет пост-инициализацию после создания экземпляра класса. """
        self._include_routers()

    def _include_routers(self):
        """
        ## Регистрирует все роутеры в приложении `FastAPI`.

        Проходит по словарю `app_routers` и включает каждый роутер
            с соответствующим префиксом.

        Raises:
            ValueError: Если `self.app` не является экземпляром `FastAPI`.
        """
        for i in self.app_routers.items():
            [self.app.include_router(r, prefix=i[0]) for r in i[-1]]


    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        """
        ## Управляет жизненным циклом приложения `FastAPI`.

        Контекстный менеджер для выполнения действий при запуске и остановке приложения.

        Args:
            app (FastAPI): Экземпляр приложения `FastAPI`.

        Yields:
            None: Контроль передается приложению во время его работы.
        """
        # Установка соединия с базой данных / обращение к какому-либо сервису
        # До запуска приложения
        # logger.info(f'Приложение запустилось на хосте: {env_config.api_host} порт: {env_config.api_port}')
        yield
        # logger.info('Приложение завершило свой цикл')
        # После выключения приложения
        # Например закрытие соединения с базой данных

    def _create_app(self) -> FastAPI:
        """
        ## Создает и настраивает экземпляр FastAPI приложения.
        
        В зависимости от окружения (production/development) настраивает
        параметры безопасности и доступности документации.
        
        Returns:
            FastAPI: Настроенный экземпляр приложения FastAPI.
        """
        is_production = env_config.env.lower() == PROD_ENV

        return FastAPI(
            lifespan=self.lifespan,
            docs_url=None if is_production else '/docs',
            redoc_url=None if is_production else '/redoc',
            openapi_url=None if is_production else '/openapi.json',
            # Отключаем отображение деталей ошибок в production
            debug=not is_production,
        )


fastapi_app = FastAPIapp()
app: FastAPI = fastapi_app.app


if env_config.env.lower() == DEV_ENV.lower():
    host_info = f"{env_config.api_host}:{env_config.api_port}"
    logger.info(  # Запись в лог информацию о запуске в dev режиме
        f"Запуск в режиме разработки на {host_info}"
    )
    if __name__ == '__main__':
        from uvicorn import run
        run(
            app='main:app',
            host=env_config.api_host,
            port=env_config.api_port,
            reload=True,
        )