from src.settings.app_settings import AppSettings

bind = f"{AppSettings.HOST}:{AppSettings.PORT}"
workers = 3
max_requests_jitter = 5
worker_class = 'uvicorn.workers.UvicornWorker'
max_requests = int(workers * 2000)
errorlog = '-'
