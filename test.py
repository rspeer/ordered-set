import pickle
import pytest
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


def test_OrderedSet():
    OrderedSet([1, 2, 3])
    # doctest want:
    # OrderedSet([1, 2, 3])


def test_OrderedSet___len__():
    assert len(OrderedSet([])) == 0
    assert len(OrderedSet([1, 2])) == 2


def test_OrderedSet___contains__():
    assert 1 in OrderedSet([1, 3, 2])
    assert 5 not in OrderedSet([1, 3, 2])


def test_OrderedSet___eq__():
    self = OrderedSet([1, 3, 2])
    assert self == [1, 3, 2]
    assert self == [1, 2, 3]
    assert self != [2, 3]
    # assert self == OrderedSet([3, 2, 1])
    assert self != OrderedSet([3, 2, 1])


def test_OrderedSet___iter__():
    list(iter(OrderedSet([1, 2, 3])))
    # doctest want:
    # [1, 2, 3]


def test_OrderedSet___reversed__():
    list(reversed(OrderedSet([1, 2, 3])))
    # doctest want:
    # [3, 2, 1]


def test_OrderedSet___getitem__():
    import pytest
    self = OrderedSet([1, 2, 3])
    assert self[0] == 1
    assert self[1] == 2
    assert self[2] == 3
    with pytest.raises(IndexError):
        self[3]
    assert self[-1] == 3
    assert self[-2] == 2
    assert self[-3] == 1
    with pytest.raises(IndexError):
        self[-4]
    assert self[::2] == [1, 3]
    assert self[0:2] == [1, 2]
    assert self[-1:] == [3]
    assert self[:] == self
    assert self[:] is not self


def test_OrderedSet_add():
    self = OrderedSet()
    self.append(3)
    print(self)
    # doctest want:
    # OrderedSet([3])


def test_OrderedSet_append():
    self = OrderedSet()
    self.append(3)
    self.append(2)
    self.append(5)
    print(self)
    # doctest want:
    # OrderedSet([3, 2, 5])


def test_OrderedSet_discard():
    self = OrderedSet([1, 2, 3])
    self.discard(2)
    print(self)
    # doctest want:
    # OrderedSet([1, 3])
    self.discard(2)
    print(self)
    # doctest want:
    # OrderedSet([1, 3])


def test_OrderedSet_pop():
    import pytest
    self = OrderedSet([2, 3, 1])
    assert self.pop() == 1
    assert self.pop() == 3
    assert self.pop() == 2
    with pytest.raises(KeyError):
        self.pop()


def test_OrderedSet_union():
    self = OrderedSet.union(OrderedSet([3, 1, 4, 1, 5]), [1, 3], [2, 0])
    print(self)
    # doctest want:
    # OrderedSet([3, 1, 4, 5, 2, 0])
    self.union([8, 9])
    # doctest want:
    # OrderedSet([3, 1, 4, 5, 2, 0, 8, 9])
    self | {10}
    # doctest want:
    # OrderedSet([3, 1, 4, 5, 2, 0, 10])
    OrderedSet.union(OrderedSet([1, 2, 3]))
    # doctest want:
    # OrderedSet([1, 2, 3])


def test_OrderedSet_intersection():
    self = OrderedSet.intersection(OrderedSet([0, 1, 2, 3]), [1, 2, 3])
    print(self)
    # doctest want:
    # OrderedSet([1, 2, 3])
    self.intersection([2, 4, 5], [1, 2, 3, 4])
    # doctest want:
    # OrderedSet([2])
    OrderedSet.intersection(OrderedSet([1, 2, 3]))
    # doctest want:
    # OrderedSet([1, 2, 3])


def test_OrderedSet_update():
    self = OrderedSet([1, 2, 3])
    self.update([3, 1, 5, 1, 4])
    print(self)
    # doctest want:
    # OrderedSet([1, 2, 3, 5, 4])


def test_OrderedSet_index():
    import pytest
    self = OrderedSet([1, 2, 3])
    assert self.index(1) == 0
    assert self.index(2) == 1
    assert self.index(3) == 2
    with pytest.raises(IndexError):
        self[4]


def test_OrderedSet_copy():
    self = OrderedSet([1, 2, 3])
    other = self.copy()
    assert self == other and self is not other


def test_OrderedSet_difference():
    OrderedSet([1, 2, 3]).difference(OrderedSet([2]))
    # doctest want:
    # OrderedSet([1, 3])
    OrderedSet([1, 2, 3]) - OrderedSet([2])
    # doctest want:
    # OrderedSet([1, 3])


def test_OrderedSet_issubset():
    OrderedSet([1, 2, 3]).issubset({1, 2})
    # doctest want:
    # False
    OrderedSet([1, 2, 3]).issubset({1, 2, 3, 4})
    # doctest want:
    # True
    OrderedSet([1, 2, 3]).issubset({1, 4, 3, 5})
    # doctest want:
    # False


def test_OrderedSet_issuperset():
    OrderedSet([1, 2]).issuperset([1, 2, 3])
    # doctest want:
    # False
    OrderedSet([1, 2, 3, 4]).issuperset({1, 2, 3})
    # doctest want:
    # True
    OrderedSet([1, 4, 3, 5]).issuperset({1, 2, 3})
    # doctest want:
    # False


def test_OrderedSet_symmetric_difference():
    self = OrderedSet([1, 4, 3, 5, 7])
    other = OrderedSet([9, 7, 1, 3, 2])
    self.symmetric_difference(other)
    # doctest want:
    # OrderedSet([4, 5, 9, 2])


def test_OrderedSet_difference_update():
    self = OrderedSet([1, 2, 3])
    self.difference_update(OrderedSet([2]))
    print(self)
    # doctest want:
    # OrderedSet([1, 3])


def test_OrderedSet_intersection_update():
    self = OrderedSet([1, 4, 3, 5, 7])
    other = OrderedSet([9, 7, 1, 3, 2])
    self.intersection_update(other)
    print(self)
    # doctest want:
    # OrderedSet([1, 3, 7])


def test_OrderedSet_symmetric_difference_update():
    self = OrderedSet([1, 4, 3, 5, 7])
    other = OrderedSet([9, 7, 1, 3, 2])
    self.symmetric_difference_update(other)
    print(self)
    # doctest want:
    # OrderedSet([4, 5, 9, 2])
