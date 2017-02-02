from datetime import timedelta

from django.utils import timezone

from celery.task import task
from reservation.models import RoomReservation


@task
def delete_old_records():
    month_ago = timezone.now() - timedelta(days=30)
    RoomReservation.objects.filter(end_date__lt=month_ago).delete()
