from datetime import timedelta

from django.utils import timezone

from reservation.models import RoomReservation
from reservation.tasks import delete_old_records


def test_not_deletes_new_reservations(fixt_reservation):
    date = timezone.now()
    fixt_reservation.start_date = date
    fixt_reservation.end_date = date + timedelta(minutes=45)
    fixt_reservation.save()
    delete_old_records()

    assert RoomReservation.objects.first() == fixt_reservation


def test_deletes_old_reservations(fixt_two_overlap_reservations):
    for reservation in fixt_two_overlap_reservations:
        reservation.end_date = timezone.now() - timedelta(days=31)
        reservation.save()
    delete_old_records()

    assert not RoomReservation.objects.exists()
