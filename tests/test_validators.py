import pytest
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.conf import settings

from reservation.validators import (
    validate_not_in_past,
    validate_not_late,
    validate_not_weekend,
    validate_working_hours
)
from reservation.serializers import RoomReservationSerializer


def test_validate_not_in_past(fixt_normal_date):
    validate_not_in_past(fixt_normal_date)


def test_validate_in_past(fixt_date_in_the_past):
    with pytest.raises(ValidationError):
        validate_not_in_past(fixt_date_in_the_past)


def test_validate_not_late(fixt_normal_date):
    validate_not_late(fixt_normal_date)


def test_validate_late(fixt_date_late_to_reserve):
    with pytest.raises(ValidationError):
        validate_not_late(fixt_date_late_to_reserve)


def test_validate_not_weekend(fixt_normal_date):
    validate_not_weekend(fixt_normal_date)


def test_validate_weekend(fixt_date_weekend):
    with pytest.raises(ValidationError):
        validate_not_weekend(fixt_date_weekend)


def test_validate_non_working_hours(fixt_normal_date):
    validate_working_hours(fixt_normal_date)


def test_validate_working_hours(fixt_date_after_work):
    with pytest.raises(ValidationError):
        validate_working_hours(fixt_date_after_work)


def test_validate_end_after_start(
        fixt_normal_date,
        fixt_reservation,
        fixt_serializer_context,
):
    # not valid date
    fixt_reservation.start_date = fixt_normal_date + timedelta(minutes=45)
    fixt_reservation.end_date = fixt_normal_date + timedelta(minutes=35)

    assert not RoomReservationSerializer(
        data=RoomReservationSerializer(fixt_reservation).data,
        context=fixt_serializer_context,
    ).is_valid()

    # valid date
    fixt_reservation.start_date = fixt_normal_date
    fixt_reservation.end_date = fixt_normal_date + timedelta(minutes=35)

    assert RoomReservationSerializer(
        data=RoomReservationSerializer(fixt_reservation).data,
        context=fixt_serializer_context,
    ).is_valid()


def test_validate_max_duration(fixt_reservation, fixt_serializer_context):

    assert RoomReservationSerializer(
        data=RoomReservationSerializer(fixt_reservation).data,
        context=fixt_serializer_context,
    ).is_valid()

    # too big duration
    fixt_reservation.end_date += settings.MAXIMUM_MEETING_DURATION

    assert not RoomReservationSerializer(
        data=RoomReservationSerializer(fixt_reservation).data,
        context=fixt_serializer_context,
    ).is_valid()


def test_validate_min_duration(fixt_reservation, fixt_serializer_context):

    assert RoomReservationSerializer(
        data=RoomReservationSerializer(fixt_reservation).data,
        context=fixt_serializer_context,
    ).is_valid()

    # too small duration
    fixt_reservation.end_date -= settings.MINIMUM_MEETING_DURATION / 2

    assert not RoomReservationSerializer(
        data=RoomReservationSerializer(fixt_reservation).data,
        context=fixt_serializer_context,
    ).is_valid()
