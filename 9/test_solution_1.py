from solution_1 import validate_number
import random


def test_validate_number() -> None:
    for _ in range(100):
        preamble = list(range(1, 26))
        random.shuffle(preamble)
        assert validate_number(preamble, 26)
        assert validate_number(preamble, 49)
        assert not validate_number(preamble, 50)
        assert not validate_number(preamble, 100)

        preamble = list(range(1, 20)) + list(range(21, 26)) + [45]
        assert validate_number(preamble, 26)
        assert not validate_number(preamble, 65)
        assert validate_number(preamble, 64)
        assert validate_number(preamble, 66)
