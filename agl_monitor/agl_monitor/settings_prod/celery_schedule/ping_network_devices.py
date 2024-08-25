from datetime import timedelta

SCHEDULE = {
    "move_pdf_examination_files": { 
        "task": "monitoring.tasks.network_devices.ping_devices",
        # "schedule": timedelta(minutes=5),
        "schedule": timedelta(minutes=1),
    },

}
