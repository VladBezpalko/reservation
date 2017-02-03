from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import status
from pytest import fixture
from freezegun import freeze_time
from reservation.models import RoomReservation


User = get_user_model()


@fixture
def fixt_data(fixt_normal_date):
    return {
        'start_date': fixt_normal_date,
        'end_date': fixt_normal_date + settings.MINIMUM_MEETING_DURATION,
        'theme': 'THEME',
        'description': 'desc',
    }


@fixture
def fixt_part_data(fixt_normal_date):
    return {
        'start_date': fixt_normal_date,
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


@freeze_time('2016-2-1')
def test_create(api_user, fixt_data):
    response = api_user.post('/reservation/', fixt_data)

    assert response.status_code == status.HTTP_201_CREATED


@freeze_time('2016-2-1')
def test_update(api_user, fixt_part_data, fixt_reservation):
    response = api_user.patch(
        '/reservation/{}/'.format(fixt_reservation.id),
        fixt_part_data
    )

    assert response.status_code == status.HTTP_200_OK


def test_update_not_owner(api_user, fixt_part_data, fixt_admin_reservation):
    response = api_user.patch(
        '/reservation/{}/'.format(fixt_admin_reservation.id),
        fixt_part_data
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@freeze_time('2016-2-1')
def test_update_admin(api_admin, fixt_part_data, fixt_reservation):
    response = api_admin.patch(
        '/reservation/{}/'.format(fixt_reservation.id),
        fixt_part_data
    )

    assert response.status_code == status.HTTP_200_OK


def test_reply_simple_user(api_user, fixt_reservation, fixt_answer_allow):
    response = api_user.post(
        '/reservation/{}/reply/'.format(fixt_reservation.id),
        fixt_answer_allow
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_reply_admin(api_admin, fixt_reservation, fixt_answer_allow):
    response = api_admin.post(
        '/reservation/{}/reply/'.format(fixt_reservation.id),
        fixt_answer_allow
    )
    fixt_reservation.refresh_from_db()

    assert fixt_reservation.answer == RoomReservation.ALLOW
    assert response.status_code == status.HTTP_200_OK


def test_reply_overlap(api_admin, fixt_reservation, fixt_overlap_reservation,
                       fixt_answer_allow):
    response = api_admin.post(
        '/reservation/{}/reply/'.format(fixt_reservation.id),
        fixt_answer_allow
    )
    fixt_reservation.refresh_from_db()

    assert fixt_reservation.answer == RoomReservation.PENDING
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_overlapping(api_admin, fixt_reservation, fixt_overlap_reservation):
    response = api_admin.get(
        '/reservation/{}/overlapping/'.format(fixt_reservation.id)
    )

    assert fixt_overlap_reservation.id == response.data[0]['id']
    assert response.status_code == status.HTTP_200_OK


def test_not_overlapping(api_admin, fixt_reservation):
    response = api_admin.get(
        '/reservation/{}/overlapping/'.format(fixt_reservation.id)
    )

    assert not response.data
    assert response.status_code == status.HTTP_200_OK
