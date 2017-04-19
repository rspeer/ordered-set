from nose.tools import eq_, raises, assert_raises
from ordered_set import OrderedSet
import pickle


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


def test_indexing():
    set1 = OrderedSet('abracadabra')
    eq_(set1[:], set1)
    eq_(set1.copy(), set1)
    assert set1[:] is set1
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


@raises(KeyError)
def test_remove_error():
    # If we .remove() an element that's not there, we get a KeyError
    set1 = OrderedSet('abracadabra')
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

    assert_raises(KeyError, set1.pop)

def test_le():
    set1 = OrderedSet([3, 5, 2])
    set2 = OrderedSet([3, 5, 2, 1])
    set3 = OrderedSet([3, 2, 5, 1])
    set4 = OrderedSet([3, 5, 2])

    assert set1 <= set2
    assert not set1 <= set3
    assert set1 <= set4

def test_ge():
    set1 = OrderedSet([3, 5, 2])
    set2 = OrderedSet([3, 5, 2, 1])
    set3 = OrderedSet([3, 2, 5, 1])
    set4 = OrderedSet([3, 5, 2])

    assert set2 >= set1
    assert not set3 >= set1
    assert set4 >= set1

def test_lt():
    set1 = OrderedSet([3, 5, 2])
    set2 = OrderedSet([3, 5, 2, 1])
    set3 = OrderedSet([3, 2, 5, 1])

    assert set1 < set2
    assert not set3 < set2

def test_gt():
    set1 = OrderedSet([3, 5, 2])
    set2 = OrderedSet([3, 5, 2, 1])
    set3 = OrderedSet([3, 2, 5, 1])

    assert set2 > set1
    assert not set3 > set1

def test_and():
    set1 = OrderedSet([3, 5, 2])
    set2 = OrderedSet([3, 5, 2, 1])
    set3 = OrderedSet([3, 2, 5, 1])
    set4 = OrderedSet([3, 5, 2])

    assert set2 & set1 == OrderedSet([3, 5, 2])
    assert set3 & set1 == OrderedSet([3])
    assert set4 & set1 == OrderedSet([3, 5, 2])

def test_sub():
    set1 = OrderedSet([3, 5, 2])
    set2 = OrderedSet([3, 5, 2, 1])
    set3 = OrderedSet([3, 5, 2])

    assert set1 - set2 == OrderedSet()
    assert set3 - set1 == OrderedSet()

def test_intersection():
    set1 = OrderedSet([3, 5,])
    set2 = OrderedSet([3, 5, 2, 1])
    set3 = OrderedSet([3, 5, 2])

    assert set3.intersection(set2, set1) == OrderedSet([3, 5])

    set3.intersection_update(set2, set1)
    assert set3 == OrderedSet([3, 5])