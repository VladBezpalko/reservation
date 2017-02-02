"""
Set of different dates for validator tests
Each date (excluding fixt_normal_date) will cause exception,
if code written right
"""
from pytest import fixture
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.http import HttpRequest


@fixture
def fixt_normal_date():
    """
    Return basic valid date.
    """
    date = timezone.now()

    # next day
    date += timedelta(days=1)

    # but not weekend
    while date.weekday() >= 5:
        # TODO:
        # while date.weekday() >= 5 and date != next_holiday():
        date += timedelta(days=1)

    # beginning of work day
    date = date.replace(
        hour=settings.WORK_HOURS[0].hour,
        minute=settings.WORK_HOURS[0].minute
    )

    # not late for reserve
    date += settings.MIN_TIME_BEFORE_RESERVATION * 2
    return date


@fixture
def fixt_date_after_work(fixt_normal_date):
    """
    Returns date with unsuitable time
    """
    date = fixt_normal_date

    # TODO:
    # add maximum time people can stay after work
    # date += timedelta(settings.MAX_TIME_STAY_AFTER_WORK)

    # 3 hours after work
    return date.replace(hour=settings.WORK_HOURS[1].hour) + timedelta(hours=3)


@fixture
def fixt_date_in_the_past(fixt_normal_date):
    """
    Hell... What was yesterday?
    """
    date = fixt_normal_date

    # In the past
    return date - timedelta(days=3)


@fixture
def fixt_date_weekend(fixt_normal_date):
    """
    Weekend, baltika, winston, bychki, sportivki, televisar
    """
    date = fixt_normal_date

    while date.weekday() != 5:
        date += timedelta(days=1)

    return date


@fixture
def fixt_date_late_to_reserve():
    """
    Only settings.MIN_TIME_BEFORE_RESERVATION / 2 before meeting
    """
    date = timezone.now()
    return date + settings.MIN_TIME_BEFORE_RESERVATION / 2


@fixture
def fixt_date_conflict_duration(fixt_normal_date):
    """
    If now 5.15, and end of working day in 5.30,
    and minimum meeting duration is 30 minutes,
    then user can't create meeting.
    """
    date = fixt_normal_date

    # end of working day
    date = date.replace(hour=settings.WORK_HOURS[1].hour,
                        minute=settings.WORK_HOURS[1].minute)

    # now very close to end of working day
    date -= settings.MINIMUM_MEETING_DURATION / 2

    return date


@fixture
def fixt_serializer_context(fixt_user):
    """
    Serializers is_valid() do not want work without this context
    """
    request = HttpRequest()
    request.user = fixt_user
    return {'request': request}
