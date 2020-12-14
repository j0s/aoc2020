from solution_1 import parse_mask
from solution_2 import set_bit, run_program


def test_parse_mask():
    assert parse_mask("1XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") == (2 ** 35, 2 ** 37 - 1)


def test_set_bit():
    assert set_bit(0, 4, True) == 16
    assert set_bit(16, 4, True) == 16
    assert set_bit(16, 3, True) == 24
    assert set_bit(16, 4, False) == 0
    assert set_bit(16, 3, False) == 16
    assert set_bit(16, 5, False) == 16
