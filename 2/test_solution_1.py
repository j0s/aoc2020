import pytest
import solution_1
from typing import List


def test_solution_1_example():
    test_input = solution_1.parse_input('test_input')
    assert solution_1.find_valid_passwords(test_input) == 2
