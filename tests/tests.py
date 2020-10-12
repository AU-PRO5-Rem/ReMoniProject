from main import increment, decrement


def test_increment():
    assert increment(3) == 4


def test_decrement():
    assert decrement(4) == 3
