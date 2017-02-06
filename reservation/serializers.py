from django.contrib.auth import get_user_model

from reservation.validators import (
    validate_end_after_start,
    validate_max_duration,
    validate_min_duration,
)
from rest_framework import serializers

from reservation.models import RoomReservation
from reservation.exceptions import NotUpdateIfApplied


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'is_staff')


class RoomReservationSerializer(serializers.ModelSerializer):
    creator = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    def update(self, instance, validated_data):
        if instance.answer == RoomReservation.ALLOW:
            raise NotUpdateIfApplied
        return super().update(instance, validated_data)

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
        validators = [
            validate_end_after_start,
            validate_max_duration,
            validate_min_duration,
        ]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomReservation
        fields = ('answer', )
