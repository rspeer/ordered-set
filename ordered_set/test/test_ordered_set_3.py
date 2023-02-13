from pathlib import Path

import mypy.api
import pytest

from ordered_set import OrderedSet

TESTS = Path(__file__).parent


def test_add():
    x = OrderedSet([1, 2, -1, "bar"])
    x.add(0)
    assert list(x) == [1, 2, -1, "bar", 0]


def test_discard():
    x = OrderedSet([1, 2, -1])
    x.discard(2)
    assert list(x) == [1, -1]


def test_discard_ignores_missing_element():
    x = OrderedSet()
    x.discard(1)  # This does not raise


def test_remove():
    x = OrderedSet([1])
    x.remove(1)
    assert not x


def test_remove_raises_missing_element():
    x = OrderedSet()
    with pytest.raises(KeyError):
        x.remove(1)


def test_getitem():
    x = OrderedSet([1, 2, -1])
    assert x[0] == 1
    assert x[1] == 2
    assert x[2] == -1
    with pytest.raises(IndexError):
        x[3]


def test_len():
    x = OrderedSet([1])
    assert len(x) == 1


def test_iter():
    for x in OrderedSet([1]):
        assert x == 1


def test_str():
    x = OrderedSet([1, 2, 3])
    assert str(x) == "{1, 2, 3}"


def test_repr():
    x = OrderedSet([1, 2, 3])
    assert repr(x) == "<OrderedSet {1, 2, 3}>"


def test_eq():
    x = OrderedSet([1, 2, 3])
    y = OrderedSet([1, 2, 3])
    assert x == y
    assert x is not y


def test_init_empty():
    x = OrderedSet()
    assert len(x) == 0
    x.add(2)
    assert len(x) == 1


def test_typing_mypy():
    """Checks the typing values with mypy."""
    fixture = TESTS / "_test_mypy.py"
    module = TESTS.parent / "ordered_set_37"
    *_, error = mypy.api.run([str(module), str(fixture)])
    assert not error
