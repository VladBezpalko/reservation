from django.utils import timezone

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


def validate_working_hours(value):
    start, end = settings.WORK_HOURS
    if not (start < value.time() < end):
        raise ValidationError(
            _('Time should be in range of working hours.'),
            code='invalid'
        )


def validate_not_in_past(value):
    if value < timezone.now():
        raise ValidationError(
            _('Time should be in future.'),
            code='invalid'
        )


def validate_not_late(value):
    min_time = settings.MIN_TIME_BEFORE_RESERVATION
    if value < timezone.now() + min_time:
        raise ValidationError(
            _('Time should be no earlier than after {!s}.'.
              format(min_time)),
            code='invalid'
        )


def validate_not_weekend(value):
    if value.weekday() >= 5:
        raise ValidationError(
            _("You can't reserve room at weekends."),
            code='invalid'
        )

