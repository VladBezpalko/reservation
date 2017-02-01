from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from reservation.models import RoomReservation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'is_staff')


class RoomReservationSerializer(serializers.ModelSerializer):
    creator = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        if (
            'start_date' in data and
            'end_date' in data and
            data['start_date'] > data['end_date']
        ):
            raise serializers.ValidationError(
                _('Start date should be earlier then end date')
            )
        return data

    class Meta:
        model = RoomReservation
        fields = (
            'id',
            'creator',
            'start_date',
            'end_date',
            'theme',
            'description',
            'answer',
        )
        read_only_fields = ('answer', )


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomReservation
        fields = ('answer', )
