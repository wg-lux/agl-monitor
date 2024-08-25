# # Celery Configuration
import json
from celery.signals import after_setup_logger

config_path = "/etc/agl-home-django/config.json"

with open(config_path) as f:
    endoreg_client_config = json.load(f)
    CELERY_BROKER_URL = config_path["CELERY_BROKER_URL"]
    CELERY_RESULT_BACKEND = config_path["CELERY_RESULT_BACKEND"]
    CELERY_ACCEPT_CONTENT = config_path["CELERY_ACCEPT_CONTENT"]
    CELERY_TASK_SERIALIZER = config_path["CELERY_TASK_SERIALIZER"]
    CELERY_RESULT_SERIALIZER = config_path["CELERY_RESULT_SERIALIZER"]
    CELERY_TIMEZONE = config_path["CELERY_TIMEZONE"]
    CELERY_BEAT_SCHEDULER = config_path["CELERY_BEAT_SCHEDULER"]
    CELERY_SIGNAL_LOGFILE_NAME = config_path["CELERY_SIGNAL_LOGFILE_NAME"]


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler(CELERY_SIGNAL_LOGFILE_NAME, maxBytes=10485760, backupCount=3)  # 10 MB per file
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)