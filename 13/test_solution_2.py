from solution_2 import parse_line, find_valid_timestamp


def test_find_valid_timestamp_simple() -> None:
    assert find_valid_timestamp(parse_line("1,3")) == 2


def test_find_valid_timestamp() -> None:
    assert find_valid_timestamp(parse_line("17,x,13,19")) == 3417
    assert find_valid_timestamp(parse_line("67,7,59,61")) == 754018
    assert find_valid_timestamp(parse_line("67,x,7,59,61")) == 779210
    assert find_valid_timestamp(parse_line("67,7,x,59,61")) == 1261476
    assert find_valid_timestamp(parse_line("1789,37,47,1889")) == 1202161486