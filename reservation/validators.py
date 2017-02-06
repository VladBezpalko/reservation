from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


def validate_working_hours(value):
    start, end = settings.WORK_HOURS
    if not (start < value.time() < end):
        raise ValidationError(_('Time should be in range of working hours.'))


def validate_not_in_past(value):
    if value < timezone.now():
        raise ValidationError(_('Time should be in future.'))


def validate_not_late(value):
    min_time = settings.MIN_TIME_BEFORE_RESERVATION
    if value < timezone.now() + min_time:
        raise ValidationError(
            _('Time should be no earlier than after {!s}.'.format(min_time))
        )


def validate_not_weekend(value):
    if value.weekday() >= 5:
        raise ValidationError(_("You can't reserve room at weekends."))


def validate_end_after_start(data):
    if 'start_date' in data and 'end_date' in data:

        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError(
                _('Start date should be earlier than end date')
            )


def validate_max_duration(data):
    if 'start_date' in data and 'end_date' in data:
        duration = data['end_date'] - data['start_date']

        if duration > settings.MAXIMUM_MEETING_DURATION:
            raise serializers.ValidationError(
                _('Duration of reservation cannot be longer '
                  'than {} hours').format(settings.MAXIMUM_MEETING_DURATION)
            )


def validate_min_duration(data):
    if 'start_date' in data and 'end_date' in data:
        duration = data['end_date'] - data['start_date']

        if duration < settings.MINIMUM_MEETING_DURATION:
            raise serializers.ValidationError(
                _('Duration of reservation cannot be shorter '
                  'than {} hours').format(settings.MINIMUM_MEETING_DURATION)
            )
