import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photogallery.settings')

app = Celery('photogallery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()