from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spinpesa.settings')

app = Celery('spinpesa')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings',namespace= 'CELERY')
app.autodiscover_tasks()
# app.conf.enable_utc = False

# app.conf.beat_schedule = {
#     # Executes every 4 minutes 
#     'create_spin_wheel_instance': { 
#          'task': 'gwheel.tasks.create_spinwheel_instance', 
#          'schedule': crontab(minute='*/4'),
#         },          
# }

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
