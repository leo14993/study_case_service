from decouple import config


class SplitIOSettings:
    SPLIT_IO_API_KEY = config('SPLIT_IO_API_KEY', cast=str, default='')
    TIME_OUT_SPLIT_IO = config('TIME_OUT_SPLIT_IO', cast=int, default=5)
    IMPRESSIONS_MODE = config('SPLIT_IO_IMPRESSIONS_MODE', default='optimized')
    CONNECTION_TIMEOUT = config('SPLIT_IO_CONNECTION_TIMEOUT', cast=int, default=1500)
    READ_TIMEOUT = config('SPLIT_IO_READ_TIMEOUT', cast=int, default=1500)
