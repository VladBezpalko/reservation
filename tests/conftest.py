from datetime import datetime
import pytest

from pytest_django.lazy_django import skip_if_no_django

from reservation.models import RoomReservation
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    """A Django Rest Framework test client instance."""
    skip_if_no_django()

    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def api_rf():
    """APIRequestFactory instance."""
    skip_if_no_django()

    from rest_framework.test import APIRequestFactory

    return APIRequestFactory()


@pytest.fixture
def fixt_user(db):
    user = User.objects.create(
        email='joe@localhost',
        username='john',
    )
    user.set_password('secret')
    user.save()
    return user


@pytest.fixture
def fixt_admin(db):
    return User.objects.create(
        email='admin@localhost',
        username='Admin',
        is_staff=True,
    )


@pytest.fixture
def fixt_reservation(db, fixt_user):
    return RoomReservation.objects.create(
        creator=fixt_user,
        theme='Test reservation 1',
        description='test test test',
        start_date=datetime(2017, 1, 13, 10, 30),
        end_date=datetime(2017, 1, 13, 11),
    )


@pytest.fixture
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