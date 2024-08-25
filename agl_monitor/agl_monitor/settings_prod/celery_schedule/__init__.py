from datetime import timedelta
from .ping_network_devices import SCHEDULE as ping_network_schedule

CELERY_BEAT_SCHEDULE = {
    # 'example_task': {
    #     'task': 'data_collector.tasks.example_task',
    #     'schedule': timedelta(minutes=1),  # change to `crontab(minute=0, hour=0)` to run daily at midnight
    # }
}

CELERY_BEAT_SCHEDULE.update(ping_network_schedule)

