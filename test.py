import collections
import itertools as it
import operator
import pickle
import random
import sys

import pytest

from ordered_set import FrozenOrderedSet, OrderedSet


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_pickle(cls):
    set1 = cls('abracadabra')
    roundtrip = pickle.loads(pickle.dumps(set1))
    assert roundtrip == set1


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_empty_pickle(cls):
    empty_set = cls()
    empty_roundtrip = pickle.loads(pickle.dumps(empty_set))
    assert empty_roundtrip == empty_set


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_order(cls):
    set1 = cls('abracadabra')
    assert len(set1) == 5
    assert set1 == cls(['a', 'b', 'r', 'c', 'd'])
    assert list(reversed(set1)) == ['d', 'c', 'r', 'b', 'a']


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_binary_operations(cls):
    set1 = cls('abracadabra')
    set2 = cls('simsalabim')
    assert set1 != set2

    assert set1 & set2 == cls(['a', 'b'])
    assert set1 | set2 == cls(['a', 'b', 'r', 'c', 'd', 's', 'i', 'm', 'l'])
    assert set1 - set2 == cls(['r', 'c', 'd'])


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_indexing(cls):
    set1 = cls('abracadabra')
    assert set1[:] == set1
    assert set1.copy() == set1
    assert set1 is set1
    assert set1[:] is not set1
    assert set1.copy() is not set1

    assert set1[[1, 2]] == cls(['b', 'r'])
    assert set1[1:3] == cls(['b', 'r'])
    assert set1.index('b') == 1
    assert set1.index(['b', 'r']) == [1, 2]
    with pytest.raises(KeyError):
        set1.index('br')


class FancyIndexTester:
    """
    Make sure we can index by a NumPy ndarray, without having to import
    NumPy.
    """

    def __init__(self, indices):
        self.indices = indices

    def __iter__(self):
        return iter(self.indices)

    def __index__(self):
        raise TypeError("NumPy arrays have weird __index__ methods")

    def __eq__(self, other):
        # Emulate NumPy being fussy about the == operator
        raise TypeError


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_fancy_index_class(cls):
    set1 = cls('abracadabra')
    indexer = FancyIndexTester([1, 0, 4, 3, 0, 2])
    assert ''.join(set1[indexer]) == 'badcar'


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_pandas_compat(cls):
    set1 = cls('abracadabra')
    assert set1.get_loc('b') == 1
    assert set1.get_indexer(['b', 'r']) == [1, 2]


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_tuples(cls):
    tup = ('tuple', 1)
    set1 = OrderedSet([tup])
    assert set1.index(tup) == 0
    assert set1[0] == tup


def test_remove():
    set1 = OrderedSet('abracadabra')

    set1.remove('a')
    set1.remove('b')

    assert set1 == OrderedSet('rcd')
    assert set1[0] == 'r'
    assert set1[1] == 'c'
    assert set1[2] == 'd'

    assert set1.index('r') == 0
    assert set1.index('c') == 1
    assert set1.index('d') == 2

    assert 'a' not in set1
    assert 'b' not in set1
    assert 'r' in set1

    # Make sure we can .discard() something that's already gone, plus
    # something that was never there
    set1.discard('a')
    set1.discard('a')


def test_remove_error():
    # If we .remove() an element that's not there, we get a KeyError
    set1 = OrderedSet('abracadabra')
    with pytest.raises(KeyError):
        set1.remove('z')


def test_clear():
    set1 = OrderedSet('abracadabra')
    set1.clear()

    assert len(set1) == 0
    assert set1 == OrderedSet()


def test_update():
    set1 = OrderedSet('abcd')
    result = set1.update('efgh')

    assert result == 7
    assert len(set1) == 8
    assert ''.join(set1) == 'abcdefgh'

    set2 = OrderedSet('abcd')
    result = set2.update('cdef')
    assert result == 5
    assert len(set2) == 6
    assert ''.join(set2) == 'abcdef'


def test_pop():
    set1 = OrderedSet('ab')
    elem = set1.pop()

    assert elem == 'b'
    elem = set1.pop()

    assert elem == 'a'

    pytest.raises(KeyError, set1.pop)


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_getitem_type_error(cls):
    set1 = cls('ab')
    with pytest.raises(TypeError):
        set1['a']


def test_update_value_error():
    set1 = OrderedSet('ab')
    with pytest.raises(ValueError):
        # noinspection PyTypeChecker
        set1.update(3)


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_empty_repr(cls):
    set1 = cls()
    assert repr(set1) == '{}()'.format(cls.__name__)


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_eq_wrong_type(cls):
    set1 = cls()
    assert set1 != 2


def test_frozen_is_hashable():
    set1 = FrozenOrderedSet("abcabc")
    assert hash(set1) == hash(set1.copy())
    assert hash(set1) == hash(("a", "b", "c"))

    set2 = FrozenOrderedSet("abcd")
    assert hash(set1) != hash(set2)
    assert hash(set1) != hash(("a", "b", "c", "d"))


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_ordered_equality(cls):
    # Ordered set checks order against sequences.
    assert cls([1, 2]) == cls([1, 2])
    assert cls([1, 2]) == [1, 2]
    assert cls([1, 2]) == (1, 2)
    assert cls([1, 2]) == collections.deque([1, 2])


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_ordered_inequality(cls):
    # Ordered set checks order against sequences.
    assert cls([1, 2]) != cls([2, 1])

    assert cls([1, 2]) != [2, 1]
    assert cls([1, 2]) != [2, 1, 1]

    assert cls([1, 2]) != (2, 1)
    assert cls([1, 2]) != (2, 1, 1)

    # Note: in Python 2.7 deque does not inherit from Sequence, but __eq__
    # contains an explicit check for this case for python 2/3 compatibility.
    assert cls([1, 2]) != collections.deque([2, 1])
    assert cls([1, 2]) != collections.deque([2, 2, 1])


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_comparisons(cls):
    # Comparison operators on sets actually test for subset and superset.
    assert cls([1, 2]) < cls([1, 2, 3])
    assert cls([1, 2]) > cls([1])

    # MutableSet subclasses aren't comparable to set on 3.3.
    if tuple(sys.version_info) >= (3, 4):
        assert cls([1, 2]) > {1}


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_unordered_equality(cls):
    # Unordered set checks order against non-sequences.
    assert cls([1, 2]) == {1, 2}
    assert cls([1, 2]) == frozenset([2, 1])

    assert cls([1, 2]) == {1: 'a', 2: 'b'}
    assert cls([1, 2]) == {1: 1, 2: 2}.keys()
    assert cls([1, 2]) == {1: 1, 2: 2}.values()

    # Corner case: OrderedDict is not a Sequence, so we don't check for order,
    # even though it does have the concept of order.
    assert cls([1, 2]) == collections.OrderedDict([(2, 2), (1, 1)])

    # Corner case: We have to treat iterators as unordered because there
    # is nothing to distinguish an ordered and unordered iterator
    assert cls([1, 2]) == iter([1, 2])
    assert cls([1, 2]) == iter([2, 1])
    assert cls([1, 2]) == iter([2, 1, 1])


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_unordered_inequality(cls):
    assert cls([1, 2]) != set([])
    assert cls([1, 2]) != frozenset([2, 1, 3])

    assert cls([1, 2]) != {2: 'b'}
    assert cls([1, 2]) != {1: 1, 4: 2}.keys()
    assert cls([1, 2]) != {1: 1, 2: 3}.values()

    # Corner case: OrderedDict is not a Sequence, so we don't check for order,
    # even though it does have the concept of order.
    assert cls([1, 2]) != collections.OrderedDict([(2, 2), (3, 1)])


def allsame_(iterable, eq=operator.eq):
    """ returns True of all items in iterable equal each other """
    iter_ = iter(iterable)
    try:
        first = next(iter_)
    except StopIteration:
        return True
    return all(eq(first, item) for item in iter_)


def check_results_(results, datas, name):
    """
    helper for binary operator tests.

    check that all results have the same value, but are different items.
    data and name are used to indicate what sort of tests is run.
    """
    if not allsame_(results):
        raise AssertionError(
            'Not all same {} for {} with datas={}'.format(results, name, datas)
        )
    for a, b in it.combinations(results, 2):
        if not isinstance(a, (bool, int)):
            assert a is not b, name + ' should all be different items'


def _operator_consistency_testdata(cls):
    """
    Predefined and random data used to test operator consistency.
    """
    # test case 1
    data1 = cls([5, 3, 1, 4])
    data2 = cls([1, 4])
    yield data1, data2

    # first set is empty
    data1 = cls([])
    data2 = cls([3, 1, 2])
    yield data1, data2

    # second set is empty
    data1 = cls([3, 1, 2])
    data2 = cls([])
    yield data1, data2

    # both sets are empty
    data1 = cls([])
    data2 = cls([])
    yield data1, data2

    # random test cases
    rng = random.Random(0)
    a, b = 20, 20
    for _ in range(10):
        data1 = cls(rng.randint(0, a) for _ in range(b))
        data2 = cls(rng.randint(0, a) for _ in range(b))
        yield data1, data2
        yield data2, data1


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_operator_consistency_isect(cls):
    for data1, data2 in _operator_consistency_testdata(cls):
        results = [data1 & data2, data1.intersection(data2)]
        if cls == OrderedSet:
            mutation_result = data1.copy()
            mutation_result.intersection_update(data2)
            results.append(mutation_result)
        check_results_(results, datas=(data1, data2), name='isect')


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_operator_consistency_difference(cls):
    for data1, data2 in _operator_consistency_testdata(cls):
        results = [data1 - data2, data1.difference(data2)]
        if cls == OrderedSet:
            mutation_result = data1.copy()
            mutation_result.difference_update(data2)
            results.append(mutation_result)
        check_results_(results, datas=(data1, data2), name='difference')


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_operator_consistency_xor(cls):
    for data1, data2 in _operator_consistency_testdata(cls):
        results = [data1 ^ data2, data1.symmetric_difference(data2)]
        if cls == OrderedSet:
            mutation_result = data1.copy()
            mutation_result.symmetric_difference_update(data2)
            results.append(mutation_result)
        check_results_(results, datas=(data1, data2), name='xor')


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_operator_consistency_union(cls):
    for data1, data2 in _operator_consistency_testdata(cls):
        results = [data1 | data2, data1.union(data2)]
        if cls == OrderedSet:
            mutation_result = data1.copy()
            mutation_result.update(data2)
            results.append(mutation_result)
        check_results_(results, datas=(data1, data2), name='union')


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_operator_consistency_subset(cls):
    for data1, data2 in _operator_consistency_testdata(cls):
        result1 = data1 <= data2
        result2 = data1.issubset(data2)
        result3 = set(data1).issubset(set(data2))
        check_results_([result1, result2, result3], datas=(data1, data2), name='subset')


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_operator_consistency_superset(cls):
    for data1, data2 in _operator_consistency_testdata(cls):
        result1 = data1 >= data2
        result2 = data1.issuperset(data2)
        result3 = set(data1).issuperset(set(data2))
        check_results_(
            [result1, result2, result3], datas=(data1, data2), name='superset'
        )


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_operator_consistency_disjoint(cls):
    for data1, data2 in _operator_consistency_testdata(cls):
        result1 = data1.isdisjoint(data2)
        result2 = len(data1.intersection(data2)) == 0
        check_results_([result1, result2], datas=(data1, data2), name='disjoint')


@pytest.mark.parametrize("cls", [OrderedSet, FrozenOrderedSet])
def test_bitwise_and_consistency(cls):
    # Specific case that was failing without explicit __and__ definition
    data1 = cls([12, 13, 1, 8, 16, 15, 9, 11, 18, 6, 4, 3, 19, 17])
    data2 = cls([19, 4, 9, 3, 2, 10, 15, 17, 11, 13, 20, 6, 14, 16, 8])
    # This requires a custom & operation apparently
    results = [data1 & data2, data1.intersection(data2)]
    if cls == OrderedSet:
        mutation_result = data1.copy()
        mutation_result.intersection_update(data2)
        results.append(mutation_result)
    check_results_([results], datas=(data1, data2), name='isect')
