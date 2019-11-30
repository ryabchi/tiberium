import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tiberium.settings')

app = Celery('tiberium')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
