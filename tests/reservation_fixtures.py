from datetime import datetime, timedelta

from django.conf import settings
from pytest import fixture

from reservation.models import RoomReservation
from django.utils import timezone


@fixture
def fixt_reservation(db, fixt_user):
    return RoomReservation.objects.create(
        creator=fixt_user,
        theme='Test reservation 1',
        description='test test test',
        start_date=datetime(2017, 1, 13, 10, 30),
        end_date=datetime(2017, 1, 13, 11),
    )


@fixture
def fixt_reservation_same_date(db, fixt_reservation):
    fixt_reservation.answer = RoomReservation.ALLOW
    fixt_reservation.save()
    return RoomReservation.objects.create(
        creator=fixt_reservation.creator,
        theme='Other theme',
        description='Other desc',
        start_date=fixt_reservation.start_date,
        end_date=fixt_reservation.end_date,
    )


@fixture
def fixt_back_to_back_reservation(db, fixt_reservation):
    return RoomReservation.objects.create(
        creator=fixt_reservation.creator,
        start_date=fixt_reservation.end_date,
        end_date=fixt_reservation.end_date + settings.MINIMUM_MEETING_DURATION,
        theme='321',
        description='123',
    )


@fixture
def fixt_not_overlap_reservation(db, fixt_user):
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
    return RoomReservation.objects.create(
        creator=fixt_user,
        start_date=date + timedelta(minutes=26),
        end_date=date + timedelta(minutes=45),
        theme='666',
        description='777'
    )


@fixture
def fixt_overlap_reservation(db, fixt_reservation, fixt_user):
    return RoomReservation.objects.create(
        creator=fixt_user,
        theme='123',
        description='456',
        start_date=fixt_reservation.start_date,
        end_date=fixt_reservation.end_date,
        answer=RoomReservation.ALLOW,
    )


@fixture
def fixt_admin_reservation(db, fixt_admin):
    return RoomReservation.objects.create(
        creator=fixt_admin,
        theme='Test reservation 2',
        description='test test test',
        start_date=datetime(2017, 1, 13, 10, 30),
        end_date=datetime(2017, 1, 13, 11),
    )


@fixture
def fixt_two_overlap_reservations(db, fixt_user):
    date = timezone.now()
    return [
        RoomReservation.objects.create(
            creator=fixt_user,
            start_date=date + timedelta(minutes=5),
            end_date=date + timedelta(minutes=10),
            theme='123',
            description='321',
            answer=RoomReservation.ALLOW,
        ),
        RoomReservation.objects.create(
            creator=fixt_user,
            start_date=date + timedelta(minutes=11),
            end_date=date + timedelta(minutes=25),
            theme='321',
            description='123',
            answer=RoomReservation.ALLOW,
        ),
        RoomReservation.objects.create(
            creator=fixt_user,
            start_date=date,
            end_date=date + timedelta(minutes=45),
            theme='666',
            description='777'
        ),
    ]
