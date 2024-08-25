# # Celery Configuration
import json
from celery.signals import after_setup_logger

agl_home_django_path = "/etc/agl-monitor/config.json"

with open(agl_home_django_path) as f:
    agl_home_django_config = json.load(f)
    CELERY_BROKER_URL = agl_home_django_config["CELERY_BROKER_URL"]
    CELERY_RESULT_BACKEND = agl_home_django_config["CELERY_RESULT_BACKEND"]
    CELERY_ACCEPT_CONTENT = agl_home_django_config["CELERY_ACCEPT_CONTENT"]
    CELERY_TASK_SERIALIZER = agl_home_django_config["CELERY_TASK_SERIALIZER"]
    CELERY_RESULT_SERIALIZER = agl_home_django_config["CELERY_RESULT_SERIALIZER"]
    CELERY_TIMEZONE = agl_home_django_config["CELERY_TIMEZONE"]
    CELERY_BEAT_SCHEDULER = agl_home_django_config["CELERY_BEAT_SCHEDULER"]


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('celery_log.log', maxBytes=10485760, backupCount=10)  # 10 MB per file
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)