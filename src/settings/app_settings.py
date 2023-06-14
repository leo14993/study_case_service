from decouple import config
from src import __version__


class AppSettings:
    HOST = config('HOST', '0.0.0.0')
    PORT = config('PORT', default=8080, cast=int)
    DEBUG = config('DEBUG', default=False, cast=bool)
    ENVIRONMENT = config('ECS_ENVIRONMENT', 'dev')
    TITLE = config('TITLE', 'Study case service')
    DESCRIPTION = config('DESCRIPTION', default='')
    ECS_APPLICATION = config('ECS_APPLICATION', 'study-case-service')
    VIRTUAL_HOST = config('VIRTUAL_HOST', 'study-case-service')
    BASE_PATH = config('BASE_PATH', default='/study-case/service')
    DATETIME_FORMAT = config('DATETIME_FORMAT', default='%Y-%m-%dT%H:%M:%S')
    VERSION = __version__
    LOGGER_NAME = 'StudyCase'
    LOGGER_APPLICATION = 'study-case-service'
    LOGGER_PRODUCT = 'study-case'
    LOGGER_OUTPUT_FORMAT = 'JSON'

    @classmethod
    def is_production_environment(cls) -> bool:
        return cls.ENVIRONMENT == 'prd'

    @classmethod
    def is_development_environment(cls) -> bool:
        return cls.ENVIRONMENT == 'dev'

    @classmethod
    def is_homologation_environment(cls) -> bool:
        return cls.ENVIRONMENT == 'hml'

    @classmethod
    def is_local_environment(cls) -> bool:
        return cls.ENVIRONMENT == 'local'


class AuthSettings:
    HOST = config('AUTH_HOST', default='localhost')
    TIMEOUT = config('AUTH_TIMEOUT', cast=int, default=5)


class ProductSettings:
    HOST = config('PRODUCT_HOST', default='localhost')
    TIMEOUT = config('PRODUCT_TIMEOUT', cast=int, default=5)
