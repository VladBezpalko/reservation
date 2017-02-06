from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ValidationError

from freezegun import freeze_time

import pytest

from reservation.validators import (
    validate_end_after_start,
    validate_max_duration,
    validate_min_duration,
    validate_not_in_past,
    validate_not_late,
    validate_not_weekend,
    validate_working_hours,
)

from rest_framework.exceptions import ValidationError as RestValidationError


@freeze_time('2016-1-29')
def test_validate_not_in_past(fixt_normal_date):
    validate_not_in_past(fixt_normal_date)


@freeze_time('2016-2-1')
def test_validate_in_past(fixt_normal_date):
    with pytest.raises(ValidationError):
        validate_not_in_past(fixt_normal_date - timedelta(days=1))


@freeze_time('2016-2-1')
def test_validate_not_late(fixt_normal_date):
    validate_not_late(fixt_normal_date)


def test_validate_late(fixt_normal_date):
    late_date = fixt_normal_date + settings.MIN_TIME_BEFORE_RESERVATION / 2
    with pytest.raises(ValidationError):
        validate_not_late(late_date)


def test_validate_not_weekend(fixt_normal_date):
    validate_not_weekend(fixt_normal_date)


def test_validate_weekend():
    with pytest.raises(ValidationError):
        saturday = datetime(2016, 2, 6)
        validate_not_weekend(saturday)


def test_validate_non_working_hours(fixt_normal_date):
    validate_working_hours(fixt_normal_date)


def test_validate_after_working_hours():
    with pytest.raises(ValidationError):
        validate_working_hours(datetime(2016, 2, 1, hour=22))


def test_validate_before_working_hours():
    with pytest.raises(ValidationError):
        validate_working_hours(datetime(2016, 2, 1, hour=6))


@pytest.fixture
def fixt_normal_data(fixt_reservation):
    return {
        'start_date': fixt_reservation.start_date,
        'end_date': fixt_reservation.end_date,
    }


def test_validate_not_end_after_start(fixt_normal_data):
    validate_end_after_start(fixt_normal_data)


def test_validate_end_after_start(fixt_reservation):
    data = {
        'start_date': fixt_reservation.end_date,
        'end_date': fixt_reservation.start_date,
    }
    with pytest.raises(RestValidationError):
        validate_end_after_start(data)


def test_validate_not_max_duration(fixt_normal_data):
    validate_max_duration(fixt_normal_data)


def test_validate_max_duration(fixt_normal_data):
    fixt_normal_data['end_date'] += settings.MAXIMUM_MEETING_DURATION
    with pytest.raises(RestValidationError):
        validate_max_duration(fixt_normal_data)


def test_validate_not_min_duration(fixt_normal_data):
    validate_min_duration(fixt_normal_data)


def test_validate_min_duration(fixt_normal_data):
    fixt_normal_data['end_date'] -= timedelta(minutes=1)
    with pytest.raises(RestValidationError):
        validate_min_duration(fixt_normal_data)
