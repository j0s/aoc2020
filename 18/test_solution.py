from solution_1 import eval_expr_str, oper_mapping


def test_open_mapping():
    assert oper_mapping["+"](1, 2) == 3


def test_eval_1():
    assert eval_expr_str("1 + 2 * 3 + 4 * 5 + 6") == 71


def test_eval_2():
    assert eval_expr_str("2 * 3 + (4 * 5)") == 26


def test_eval_3():
    assert eval_expr_str("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437


def test_eval_4():
    assert eval_expr_str("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240


def test_eval_5():
    assert eval_expr_str("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632
