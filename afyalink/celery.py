import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afyalink.settings')

app = Celery('afyalink')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Schedule periodic tasks
app.conf.beat_schedule = {
    'send-appointment-reminders': {
        'task': 'core.tasks.send_appointment_reminders',
        'schedule': crontab(hour=8, minute=0),  # Every day at 8 AM
    },
    'send-bill-reminders': {
        'task': 'core.tasks.send_bill_reminders',
        'schedule': crontab(hour=10, minute=0),  # Every day at 10 AM
    },
    'update-appointment-status': {
        'task': 'core.tasks.update_appointment_status',
        'schedule': crontab(minute='*/30'),  # Every 30 minutes
    },
}
