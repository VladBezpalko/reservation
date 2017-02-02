import pytest

from django.core.exceptions import ValidationError

from reservation.validators import (
    validate_not_in_past,
    validate_not_late,
    validate_not_weekend,
    validate_working_hours
)


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
