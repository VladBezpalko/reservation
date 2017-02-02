from datetime import datetime
from pytest import fixture

from pytest_django.lazy_django import skip_if_no_django

from reservation.models import RoomReservation
from django.contrib.auth import get_user_model

User = get_user_model()

pytest_plugins = ["date_fixtures"]


@fixture
def api_client():
    """A Django Rest Framework test client instance."""
    skip_if_no_django()

    from rest_framework.test import APIClient

    return APIClient()


@fixture
def api_rf():
    """APIRequestFactory instance."""
    skip_if_no_django()

    from rest_framework.test import APIRequestFactory

    return APIRequestFactory()


@fixture
def fixt_user(db):
    user = User.objects.create(
        email='joe@localhost',
        username='john',
    )
    user.set_password('secret')
    user.save()
    return user


@fixture
def fixt_admin(db):
    return User.objects.create(
        email='admin@localhost',
        username='Admin',
        is_staff=True,
    )


@fixture
def api_user(api_client, fixt_user):
    api_client.force_authenticate(user=fixt_user)
    return api_client


@fixture
def api_admin(api_client, fixt_admin):
    api_client.force_authenticate(user=fixt_admin)
    return api_client


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
def fixt_overlap_reservation(db, fixt_reservation, fixt_admin):
    return RoomReservation.objects.create(
        creator=fixt_admin,
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
def fixt_reservations(db, fixt_user):
    return [
        RoomReservation.objects.create(
            creator=fixt_user,
            theme='Test reservation 1',
            description='test test test',
            start_date=datetime(2017, 1, 13, 10, 30),
            end_date=datetime(2017, 1, 13, 11),
            answer=RoomReservation.ALLOW,
        ),
        RoomReservation.objects.create(
            creator=fixt_user,
            theme='Test reservation 2',
            description='test test test',
            start_date=datetime(2017, 1, 13, 10),
            end_date=datetime(2017, 1, 13, 11),
            answer=RoomReservation.ALLOW,
        ),
        RoomReservation.objects.create(
            creator=fixt_user,
            theme='Test reservation 3',
            description='test test test',
            start_date=datetime(2017, 1, 13, 12),
            end_date=datetime(2017, 1, 13, 13),
            answer=RoomReservation.ALLOW,
        ),
    ]
