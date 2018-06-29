import pickle
import pytest
import collections
import sys
from ordered_set import OrderedSet


def eq_(item1, item2):
    # replacement for a nosetest util
    assert item1 == item2


def test_pickle():
    set1 = OrderedSet('abracadabra')
    roundtrip = pickle.loads(pickle.dumps(set1))
    assert roundtrip == set1


def test_empty_pickle():
    empty_oset = OrderedSet()
    empty_roundtrip = pickle.loads(pickle.dumps(empty_oset))
    assert empty_roundtrip == empty_oset


def test_order():
    set1 = OrderedSet('abracadabra')
    eq_(len(set1), 5)
    eq_(set1, OrderedSet(['a', 'b', 'r', 'c', 'd']))
    eq_(list(reversed(set1)), ['d', 'c', 'r', 'b', 'a'])


def test_binary_operations():
    set1 = OrderedSet('abracadabra')
    set2 = OrderedSet('simsalabim')
    assert set1 != set2

    eq_(set1 & set2, OrderedSet(['a', 'b']))
    eq_(set1 | set2, OrderedSet(['a', 'b', 'r', 'c', 'd', 's', 'i', 'm', 'l']))
    eq_(set1 - set2, OrderedSet(['r', 'c', 'd']))


def test_indexing():
    set1 = OrderedSet('abracadabra')
    eq_(set1[:], set1)
    eq_(set1.copy(), set1)
    assert set1 is set1
    assert set1[:] is not set1
    assert set1.copy() is not set1

    eq_(set1[[1, 2]], OrderedSet(['b', 'r']))
    eq_(set1[1:3], OrderedSet(['b', 'r']))
    eq_(set1.index('b'), 1)
    eq_(set1.index(['b', 'r']), [1, 2])
    try:
        set1.index('br')
        assert False, "Looking up a nonexistent key should be a KeyError"
    except KeyError:
        pass


def test_tuples():
    set1 = OrderedSet()
    tup = ('tuple', 1)
    set1.add(tup)
    eq_(set1.index(tup), 0)
    eq_(set1[0], tup)


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


def test_getitem_type_error():
    set1 = OrderedSet('ab')
    with pytest.raises(TypeError):
        set1['a']


def test_update_value_error():
    set1 = OrderedSet('ab')
    with pytest.raises(ValueError):
        set1.update(3)


def test_empty_repr():
    set1 = OrderedSet()
    assert repr(set1) == 'OrderedSet()'


def test_eq_wrong_type():
    set1 = OrderedSet()
    assert set1 != 2


def test_ordered_equality():
    # Ordered set checks order against sequences.
    assert OrderedSet([1, 2]) == OrderedSet([1, 2])
    assert OrderedSet([1, 2]) == [1, 2]
    assert OrderedSet([1, 2]) == (1, 2)
    assert OrderedSet([1, 2]) == collections.deque([1, 2])


def test_ordered_inequality():
    # Ordered set checks order against sequences.
    assert OrderedSet([1, 2]) != OrderedSet([2, 1])

    assert OrderedSet([1, 2]) != [2, 1]
    assert OrderedSet([1, 2]) != [2, 1, 1]

    assert OrderedSet([1, 2]) != (2, 1)
    assert OrderedSet([1, 2]) != (2, 1, 1)

    # Note: in Python 2.7 deque does not inherit from Sequence, but __eq__
    # contains an explicit check for this case for python 2/3 compatibility.
    assert OrderedSet([1, 2]) != collections.deque([2, 1])
    assert OrderedSet([1, 2]) != collections.deque([2, 2, 1])


def test_comparisons():
    # Comparison operators on sets actually test for subset and superset.
    assert OrderedSet([1, 2]) < OrderedSet([1, 2, 3])
    assert OrderedSet([1, 2]) > OrderedSet([1])

    # MutableSet subclasses aren't comparable to set on 3.3.
    if tuple(sys.version_info) >= (3, 4):
        assert OrderedSet([1, 2]) > {1}


def test_unordered_equality():
    # Unordered set checks order against non-sequences.
    assert OrderedSet([1, 2]) == set([1, 2])
    assert OrderedSet([1, 2]) == frozenset([2, 1])

    assert OrderedSet([1, 2]) == {1: 'a', 2: 'b'}
    assert OrderedSet([1, 2]) == {1: 1, 2: 2}.keys()
    assert OrderedSet([1, 2]) == {1: 1, 2: 2}.values()

    # Corner case: OrderedDict is not a Sequence, so we don't check for order,
    # even though it does have the concept of order.
    assert OrderedSet([1, 2]) == collections.OrderedDict([(2, 2), (1, 1)])

    # Corner case: We have to treat iterators as unordered because there
    # is nothing to distinguish an ordered and unordered iterator
    assert OrderedSet([1, 2]) == iter([1, 2])
    assert OrderedSet([1, 2]) == iter([2, 1])
    assert OrderedSet([1, 2]) == iter([2, 1, 1])


def test_unordered_inequality():
    assert OrderedSet([1, 2]) != set([])
    assert OrderedSet([1, 2]) != frozenset([2, 1, 3])

    assert OrderedSet([1, 2]) != {2: 'b'}
    assert OrderedSet([1, 2]) != {1: 1, 4: 2}.keys()
    assert OrderedSet([1, 2]) != {1: 1, 2: 3}.values()

    # Corner case: OrderedDict is not a Sequence, so we don't check for order,
    # even though it does have the concept of order.
    assert OrderedSet([1, 2]) != collections.OrderedDict([(2, 2), (3, 1)])


def test_bitwise_and():
    """
    # xdoctest ~/code/ordered-set/test.py test_bitwise_and
    pytest ~/code/ordered-set/test.py -s -k test_bitwise_and
    """
    import operator
    import itertools as it

    def allsame(iterable, eq=operator.eq):
            iter_ = iter(iterable)
            try:
                first = next(iter_)
            except StopIteration:
                return True
            return all(eq(first, item) for item in iter_)

    def check_results(*results, **kw):
        name = kw.get('name', 'set test')
        datas = kw.get('datas', [])
        if not allsame(results):
            raise AssertionError('Not all same {} for {} with datas={}'.format(
                results, name, datas))
        for a, b in it.combinations(results, 2):
            if not isinstance(a, (bool, int)):
                assert a is not b, name + ' should all be different items'

    data1 = OrderedSet([12, 13, 1, 8, 16, 15, 9, 11, 18, 6, 4, 3, 19, 17])
    data2 = OrderedSet([19, 4, 9, 3, 2, 10, 15, 17, 11, 13, 20, 6, 14, 16, 8])
    print('\ndata1 = {!r}'.format(data1))
    print('data2 = {!r}'.format(data2))
    result1 = data1.copy()
    result1.intersection_update(data2)
    # This requires a custom & operation apparently
    result2 = (data1 & data2)
    result3 = (data1.intersection(data2))
    print('result1 = {!r}'.format(result1))
    print('result2 = {!r}'.format(result2))
    print('result3 = {!r}\n'.format(result3))
    # result1 = OrderedSet([13, 8, 16, 15, 9, 11, 6, 4, 3, 19, 17])
    # result2 = OrderedSet([13, 8, 16, 15, 9, 11, 6, 4, 3, 19, 17])
    # result3 = OrderedSet([13, 8, 16, 15, 9, 11, 6, 4, 3, 19, 17])

    check_results(result1, result2, result3, datas=(data1, data2),
                  name='isect')
