from facts import __author__


def test_author():
    assert type(__author__) == str
    assert "@fintechstudios.com" in __author__
