import pytest
import solution_2
from typing import List


def test_solution_1_example():
    test_input = solution_2.parse_input('test_input')
    assert solution_2.find_valid_passwords(test_input) == 2
