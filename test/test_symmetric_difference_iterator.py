import pytest

from ordered_set import OrderedSet


@pytest.mark.parametrize(
    "left, right, expected",
    [
        ([3, 1, 2], [2, 4, 4, 1, 5], [3, 4, 5]),
        ([], [2, 1, 2], [2, 1]),
        ([3, 1, 2], [], [3, 1, 2]),
        ([3, 1, 2], [1, 2, 3], []),
    ],
)
def test_symmetric_difference_with_one_shot_operand(left, right, expected):
    values = OrderedSet(left)
    result = values.symmetric_difference(iter(right))
    assert list(result) == expected
    assert result == values ^ iter(right)
    assert result is not values
    assert list(values) == left
    for index, item in enumerate(result):
        assert result.index(item) == index


def test_symmetric_difference_consumes_generator_once_and_preserves_subclass():
    class CustomSet(OrderedSet):
        pass

    visited = []

    def other():
        for value in [2, 4, 4, 5]:
            visited.append(value)
            yield value

    result = CustomSet([3, 2]).symmetric_difference(other())
    assert isinstance(result, CustomSet)
    assert list(result) == [3, 4, 5]
    assert visited == [2, 4, 4, 5]
