import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule  = {
    'action_every_month_8am': {
        'task' : 'action',
        'schedule' : crontab(hour = 8, minute = 0, day_of_month = 1), 
        'args' : (), 
    }, 
}


if os.name == 'nt':  
    app.conf.worker_pool = 'solo'