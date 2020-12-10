import pytest
import solution_2
from typing import List


def test_solution_2_notfound():
    with pytest.raises(BaseException):
        solution_2.find_numbers_totalling([1, 2, 3], 2)


def test_solution_2_simple():
    assert solution_2.find_numbers_totalling([1, 2, 3], 6) == (1, 2, 3)


def test_solution_2_example():
    test_input = solution_2.parse_input('test_input')
    assert solution_2.find_numbers_totalling(
        test_input, 2020) == (979, 366, 675)
