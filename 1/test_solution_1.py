import pytest
import solution_1
from typing import List


def test_solution_1():
    with pytest.raises(BaseException):
        solution_1.find_numbers_totalling([1, 2, 3], 2)

    assert solution_1.find_numbers_totalling([1, 2, 3], 4) == (1, 3)

    test_input = solution_1.parse_input('test_input')
    assert solution_1.find_numbers_totalling(test_input, 2020) == (1721, 299)
    assert 1721 * 299 == 514579
