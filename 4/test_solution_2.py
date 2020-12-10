from solution_2 import validators


def test_byr():
    assert validators["byr"]("2002")
    assert not validators["byr"]("2003")


def test_hgt():
    assert validators["hgt"]("60in")
    assert validators["hgt"]("190cm")
    assert not validators["hgt"]("190in")
    assert not validators["hgt"]("190")


def test_hcl():
    assert validators["hcl"]("#123abc")
    assert not validators["hcl"]("#123abz")
    assert not validators["hcl"]("123abc")


def test_ecl():
    assert validators["ecl"]("brn")
    assert not validators["ecl"]("wat")


def test_pid():
    assert validators["pid"]("000000001")
    assert not validators["pid"]("0123456789")
