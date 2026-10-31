from typing import Iterator

from ordered_set import OrderedSet


def test_update_accepts_iterables() -> None:
    values: OrderedSet[int] = OrderedSet([1])

    index: int = values.update(value for value in [2, 1, 3])
    assert list(values) == [1, 2, 3]
    assert index == 2

    index = values.update(iter([4, 2]))
    assert list(values) == [1, 2, 3, 4]
    assert index == 1

    class IterableOnly:
        def __iter__(self) -> Iterator[int]:
            yield 5
            yield 3

    index = values.update(IterableOnly())
    assert list(values) == [1, 2, 3, 4, 5]
    assert index == 2
