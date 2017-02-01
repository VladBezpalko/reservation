from django_filters.rest_framework import FilterSet

from reservation.models import RoomReservation


class RoomReservationFilter(FilterSet):
    class Meta:
        model = RoomReservation
        fields = {
            'answer': ['exact'],
            'start_date': ['lt'],
            'end_date': ['gt'],
            'creator_id': ['exact'],
        }
