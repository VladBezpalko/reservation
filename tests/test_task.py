from datetime import timedelta

from django.utils import timezone

from reservation.tasks import delete_old_records
from reservation.models import RoomReservation


def test_not_deletes_new_reservations(fixt_reservation):
    date = timezone.now()
    fixt_reservation.start_date = date
    fixt_reservation.end_date = date + timedelta(minutes=45)
    fixt_reservation.save()
    delete_old_records()

    assert RoomReservation.objects.first() == fixt_reservation


def test_deletes_old_reservations(fixt_reservations):
    for reservation in fixt_reservations:
        reservation.end_date = timezone.now() - timedelta(days=31)
        reservation.save()
    delete_old_records()

    assert not RoomReservation.objects.exists()
