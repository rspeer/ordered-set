import pytest

from ordered_set import OrderedSet


def test_append_uses_subclass_add_and_returns_its_index():
    class UppercaseSet(OrderedSet):
        def add(self, key):
            return super().add(key.upper())

    values = UppercaseSet()
    assert values.append("alice") == 0
    assert values.append("ALICE") == 0
    assert values.append("bob") == 1
    assert list(values) == ["ALICE", "BOB"]
    assert values.index("BOB") == 1


def test_append_preserves_subclass_validation():
    class PositiveSet(OrderedSet):
        def add(self, key):
            if key <= 0:
                raise ValueError("positive values only")
            return super().add(key)

    values = PositiveSet([1])
    with pytest.raises(ValueError, match="positive values only"):
        values.append(0)
    assert list(values) == [1]
    assert 0 not in values
