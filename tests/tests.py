from main import increment, decrement


def test_increment():
    assert increment(5) == 6


def test_decrement():
    assert decrement(4) == 3
