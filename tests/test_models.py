from reservation.models import RoomReservation


def test_room_reservation(fixt_reservation):
    assert fixt_reservation.answer == RoomReservation.PENDING


def test_overlapping(fixt_reservations):
    print(fixt_reservations)
    print(RoomReservation.objects.all())
    assert False
    print(fixt_reservations[0])
    assert print(fixt_reservations[0])
