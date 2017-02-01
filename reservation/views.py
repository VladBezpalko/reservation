from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import detail_route
from rest_framework.filters import DjangoFilterBackend, OrderingFilter

from reservation.exceptions import RecordOverlap
from reservation.filters import RoomReservationFilter
from reservation.models import RoomReservation
from reservation.permissions import IsOwnerOrStaffOrReadOnly
from reservation.serializers import (
    AnswerSerializer, RoomReservationSerializer, UserSerializer,
)

User = get_user_model()


class RoomReservationViewSet(ModelViewSet):
    queryset = RoomReservation.objects.all()
    serializer_class = RoomReservationSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrStaffOrReadOnly, )
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = RoomReservationFilter
    ordering_fields = ('start_date', )

    @detail_route(methods=['POST'], permission_classes=[IsAdminUser])
    def reply(self, request, pk=None):
        assert pk is not None

        instance = self.get_object()
        answer_serializer = AnswerSerializer(data=request.data)
        answer_serializer.is_valid(raise_exception=True)
        answer = answer_serializer.validated_data['answer']

        if answer == RoomReservation.ALLOW and instance.is_overlap:
            raise RecordOverlap

        instance.answer = answer
        instance.save(update_fields=['answer'])
        serializer = RoomReservationSerializer(instance)
        return Response(serializer.data)

    @detail_route(methods=['GET'], permission_classes=[IsAdminUser])
    def overlapping(self, request, pk=None):
        """
        Это можно делать и на фронте, в фильтре это заложено.
        Сделано, на всякий случай, для удобства фронтендщика
        (передавать id записи, а не datetime's)
        """
        assert pk is not None

        instance = self.get_object()
        overlapping = instance.overlapping_list
        serializer = RoomReservationSerializer(overlapping, many=True)
        return Response(serializer.data)


class UsersViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
