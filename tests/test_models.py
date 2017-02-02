from datetime import timedelta

from django.utils import timezone
from django.conf import settings

from reservation.models import RoomReservation


def test_room_reservation(fixt_reservation):
    assert fixt_reservation.answer == RoomReservation.PENDING


def test_simple_overlapping(db, fixt_user):
    """
    Simple multiple overlapping
    """
    date = timezone.now()
    RoomReservation.objects.bulk_create([
        RoomReservation(
            creator=fixt_user,
            start_date=date + timedelta(minutes=5),
            end_date=date + timedelta(minutes=10),
            theme='123',
            description='321',
            answer=RoomReservation.ALLOW,
        ),
        RoomReservation(
            creator=fixt_user,
            start_date=date + timedelta(minutes=11),
            end_date=date + timedelta(minutes=25),
            theme='321',
            description='123',
            answer=RoomReservation.ALLOW,
        )]
    )

    assert RoomReservation(
        creator=fixt_user,
        start_date=date,
        end_date=date + timedelta(minutes=45),
        theme='666',
        description='777'
    ).overlapping_list.count() == 2


def test_not_overlaps(db, fixt_user):
    date = timezone.now()
    RoomReservation.objects.bulk_create([
        RoomReservation(
            creator=fixt_user,
            start_date=date + timedelta(minutes=5),
            end_date=date + timedelta(minutes=10),
            theme='123',
            description='321',
            answer=RoomReservation.ALLOW,
        ),
        RoomReservation(
            creator=fixt_user,
            start_date=date + timedelta(minutes=11),
            end_date=date + timedelta(minutes=25),
            theme='321',
            description='123',
            answer=RoomReservation.ALLOW,
        )]
    )

    assert not RoomReservation(
        creator=fixt_user,
        start_date=date + timedelta(minutes=26),
        end_date=date + timedelta(minutes=45),
        theme='666',
        description='777'
    ).is_overlap


def test_same_date_overlaps(db, fixt_user):
    """
    Reservations with equal date must overlaps
    """
    date = timezone.now()
    RoomReservation.objects.create(
        creator=fixt_user,
        start_date=date,
        end_date=date + settings.MINIMUM_MEETING_DURATION,
        theme='123',
        description='321',
        answer=RoomReservation.ALLOW
    )
    reservation = RoomReservation.objects.create(
        creator=fixt_user,
        start_date=date,
        end_date=date + settings.MINIMUM_MEETING_DURATION,
        theme='321',
        description='123',
    )

    assert reservation.is_overlap
    assert reservation.overlapping_list[0].theme == '123'


def test_back_to_back_not_overlaps(db, fixt_user):
    """
    One reservation ends in 19:00:00,
    and another starts at 19:00:00,
    they does not overlaps
    """
    date = timezone.now()
    RoomReservation.objects.create(
        creator=fixt_user,
        start_date=date,
        end_date=date + settings.MINIMUM_MEETING_DURATION,
        theme='123',
        description='321',
        answer=RoomReservation.ALLOW
    )
    reservation = RoomReservation.objects.create(
        creator=fixt_user,
        start_date=date + settings.MINIMUM_MEETING_DURATION,
        end_date=date + settings.MINIMUM_MEETING_DURATION * 2,
        theme='321',
        description='123',
    )

    assert not reservation.is_overlap
