from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from reservation.validators import (
    validate_working_hours, validate_not_in_past, validate_not_late
)


class RoomReservation(models.Model):
    DENY = 0
    ALLOW = 1
    PENDING = 2

    ANSWER_CHOICES = (
        (DENY, _('Deny')),
        (ALLOW, _('Allow')),
        (PENDING, _('Pending')),
    )

    DATETIME_VALIDATORS = (
        validate_working_hours,
        validate_not_in_past,
        validate_not_late
    )

    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    start_date = models.DateTimeField(validators=DATETIME_VALIDATORS)
    end_date = models.DateTimeField(validators=DATETIME_VALIDATORS)
    theme = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    answer = models.IntegerField(
        choices=ANSWER_CHOICES,
        default=PENDING
    )

    @property
    def overlapping_list(self):
        return RoomReservation.objects.filter(
            start_date__lt=self.end_date,
            end_date__gt=self.start_date,
            answer=RoomReservation.ALLOW,
        )

    # TODO: optimize filter (db indexing or caching)

    @property
    def is_overlap(self):
        return self.overlapping_list.exists()
