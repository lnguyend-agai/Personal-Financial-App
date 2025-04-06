from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# config Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')

# Using config from settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto find task
app.autodiscover_tasks()