from datetime import datetime

from django.contrib.auth import get_user_model

from rest_framework import status
from pytest import fixture

from reservation.models import RoomReservation
from reservation.serializers import RoomReservationSerializer

User = get_user_model()


def dict_equals(x, y):
    diff = set(dict(x.items())) - set(dict(y.items()))
    return diff == set()


@fixture
def fixt_data():
    return {
        'start_date': datetime(2017, 2, 12, 17, 00),
        'end_date': datetime(2017, 2, 12, 17, 20),
        'theme': 'THEME',
        'description': 'desc',
    }


@fixture
def fixt_part_data():
    return {
        'start_date': datetime(2017, 2, 12, 15, 00),
        'theme': 'theme',
    }


@fixture
def fixt_answer_allow():
    return {
        'answer': RoomReservation.ALLOW,
    }


def test_create_anon(api_client, fixt_data):
    response = api_client.post('/reservation/', fixt_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create(api_client, fixt_user, fixt_data):
    api_client.force_authenticate(user=fixt_user)
    response = api_client.post('/reservation/', fixt_data)
    assert response.status_code == status.HTTP_201_CREATED


def test_update(api_client, fixt_user, fixt_part_data, fixt_reservation):
    api_client.force_authenticate(user=fixt_user)
    response = api_client.patch(
        '/reservation/{}/'.format(fixt_reservation.id),
        fixt_part_data
    )
    assert response.status_code == status.HTTP_200_OK


def test_reply_simple_user(api_client, fixt_user, fixt_reservation,
                           fixt_answer_allow):
    api_client.force_authenticate(user=fixt_user)
    response = api_client.post(
        '/reservation/{}/reply/'.format(fixt_reservation.id),
        fixt_answer_allow
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_reply_admin(api_client, fixt_admin, fixt_reservation,
                     fixt_answer_allow):
    api_client.force_authenticate(user=fixt_admin)
    response = api_client.post(
        '/reservation/{}/reply/'.format(fixt_reservation.id),
        fixt_answer_allow
    )
    fixt_reservation.refresh_from_db()

    assert fixt_reservation.answer == RoomReservation.ALLOW
    assert response.status_code == status.HTTP_200_OK


def test_reply_overlap(api_client, fixt_admin, fixt_reservation,
                       fixt_answer_allow):
    RoomReservation.objects.create(
        creator=fixt_admin,
        theme='123',
        description='456',
        start_date=fixt_reservation.start_date,
        end_date=fixt_reservation.end_date,
        answer=RoomReservation.ALLOW,
    )
    api_client.force_authenticate(user=fixt_admin)
    response = api_client.post(
        '/reservation/{}/reply/'.format(fixt_reservation.id),
        fixt_answer_allow
    )
    fixt_reservation.refresh_from_db()

    assert fixt_reservation.answer == RoomReservation.PENDING
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_overlapping(api_client, fixt_admin, fixt_reservation):
    overlapped = RoomReservation.objects.create(
        creator=fixt_admin,
        theme='123',
        description='456',
        start_date=fixt_reservation.start_date,
        end_date=fixt_reservation.end_date,
        answer=RoomReservation.ALLOW,
    )
    api_client.force_authenticate(user=fixt_admin)
    response = api_client.get(
        '/reservation/{}/overlapping/'.format(fixt_reservation.id)
    )
    serialized = RoomReservationSerializer(overlapped)

    assert dict_equals(serialized.data, response.data[0])
    assert response.status_code == status.HTTP_200_OK
