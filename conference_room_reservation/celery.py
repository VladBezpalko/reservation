import os

from celery import Celery

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'conference_room_reservation.settings'
)

app = Celery('conference_room_reservation')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()
