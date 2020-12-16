from solution_1 import get_last_number


def test_get_sequence():
    assert get_last_number([0, 3, 6], 2020) == 436
    assert get_last_number([1, 3, 2], 2020) == 1
    assert get_last_number([2, 1, 3], 2020) == 10
    assert get_last_number([1, 2, 3], 2020) == 27
    assert get_last_number([2, 3, 1], 2020) == 78
    assert get_last_number([3, 2, 1], 2020) == 438
    assert get_last_number([3, 1, 2], 2020) == 1836
