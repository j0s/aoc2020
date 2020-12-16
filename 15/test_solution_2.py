from solution_2 import get_last_number


def test_get_sequence():
    assert get_last_number([0, 3, 6], 30000000) == 175594
    assert get_last_number([1, 3, 2], 30000000) == 2578
    assert get_last_number([2, 1, 3], 30000000) == 3544142
    assert get_last_number([1, 2, 3], 30000000) == 261214
    assert get_last_number([2, 3, 1], 30000000) == 6895259
    assert get_last_number([3, 2, 1], 30000000) == 18
    assert get_last_number([3, 1, 2], 30000000) == 362
