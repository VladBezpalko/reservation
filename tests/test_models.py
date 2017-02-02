
def test_simple_overlapping(db, fixt_two_overlap_reservations):
    """
    Simple multiple overlapping
    """
    *_, not_allowed = fixt_two_overlap_reservations

    assert not_allowed.is_overlap
    assert not_allowed.overlapping_list.count() == 2


def test_not_overlaps(db, fixt_not_overlap_reservation):

    assert not fixt_not_overlap_reservation.is_overlap
    assert not fixt_not_overlap_reservation.overlapping_list


def test_same_date_overlaps(db, fixt_reservation_same_date):
    """
    Reservations with equal date must overlaps
    """

    assert fixt_reservation_same_date.is_overlap


def test_back_to_back_not_overlaps(db, fixt_back_to_back_reservation):
    """
    One reservation ends in 19:00:00,
    and another starts at 19:00:00,
    they does not overlaps
    """

    assert not fixt_back_to_back_reservation.is_overlap
