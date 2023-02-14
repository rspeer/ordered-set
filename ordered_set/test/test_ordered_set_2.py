# The following tests are based on
# https://github.com/simonpercivall/orderedset/blob/master/tests/test_orderedset.py
# Thus shall be under the license:
# https://github.com/simonpercivall/orderedset/blob/master/LICENSE

import copy
import gc
import pickle
import weakref

import pytest

from ordered_set.test import (
    all_sets,
    ordered_sets,
    stable_and_ordered_sets,
    stableeq_and_ordered_sets,
    stableeq_sets,
)
from ordered_set.test.pytest_util import (
    assertEqual,
    assertFalse,
    assertGreater,
    assertGreaterEqual,
    assertIsNot,
    assertLess,
    assertLessEqual,
    assertNotEqual,
    assertNotIn,
    assertTrue,
)

datasets = [list(range(10))]


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", all_sets)
def test_add_new(set_t, lst: list):
    oset = set_t(lst)
    lst = copy.copy(lst)

    item = 10
    lst.append(item)
    oset.add(item)

    assertEqual(list(oset), lst)


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", all_sets)
def test_add_existing(set_t, lst: list):
    oset = set_t(lst)
    lst = copy.copy(lst)

    oset.add(1)
    oset.add(3)
    assertEqual(list(oset), lst)


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", all_sets)
def test_discard(set_t, lst: list):
    oset = set_t([1, 2, 3])

    oset.discard(1)
    assertNotIn(1, oset)

    oset.discard(4)


@pytest.mark.parametrize("set_t", stable_and_ordered_sets)
def test_pop(set_t):
    oset = set_t([1, 2, 3])

    v = oset.pop()
    assertEqual(v, 3)
    assertNotIn(v, oset)

    v = oset.popitem(last=False)
    assertEqual(v, 1)
    assertNotIn(v, oset)


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", all_sets)
def test_remove(set_t, lst: list):
    oset = set_t(lst)
    lst = copy.copy(lst)

    oset.remove(3)
    lst.remove(3)

    assertEqual(list(oset), lst)


@pytest.mark.parametrize("set_t", all_sets)
def test_clear(set_t):
    val = frozenset([1])

    oset = set_t()
    ws = weakref.WeakKeyDictionary()

    oset.add(val)
    ws[val] = 1
    oset.clear()

    assertEqual(list(oset), [])

    del val
    gc.collect()
    assertEqual(list(ws), [])


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", all_sets)
def test_copy(set_t, lst: list):
    oset1 = set_t(lst)
    oset2 = oset1.copy()

    assertIsNot(oset1, oset2)
    assertEqual(oset1, oset2)

    oset1.clear()
    assertNotEqual(oset1, oset2)


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", all_sets)
def test_reduce(set_t, lst: list):
    oset = set_t(lst)
    oset2 = copy.copy(oset)
    assertEqual(oset, oset2)

    oset3 = pickle.loads(pickle.dumps(oset))
    assertEqual(oset, oset3)

    oset.add(-1)
    assertNotEqual(oset, oset2)


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", stable_and_ordered_sets)
def test_difference_and_update(set_t, lst: list):
    list1 = [1, 2, 3]
    list2 = [3, 4, 5]
    oset1 = set_t(list1)
    oset2 = set_t(list2)

    # right hand
    oset3 = oset2 - list1
    assertEqual(oset3, set_t([4, 5]))
    assertEqual(oset2.difference(oset1), oset3)

    oset3 = list2 - oset1
    assertEqual(oset3, set_t([4, 5]))
    assertEqual(oset2.difference(oset1), oset3)

    oset3 = oset1 - oset2
    assertEqual(oset3, set_t([1, 2]))
    assertEqual(oset1.difference(oset2), oset3)

    # left hand
    oset3 = oset1 - list2
    assertEqual(oset3, set_t([1, 2]))
    assertEqual(oset1.difference(oset2), oset3)

    oset3 = list1 - oset2
    assertEqual(oset3, set_t([1, 2]))
    assertEqual(oset1.difference(oset2), oset3)

    oset4 = oset1.copy()
    oset4 -= oset2
    assertEqual(oset4, oset3)

    oset5 = oset1.copy()
    oset5.difference_update(oset2)
    assertEqual(oset5, oset3)


@pytest.mark.parametrize("set_t", all_sets)
def test_intersection_and_update(set_t):
    oset1 = set_t([1, 2, 3])
    oset2 = set_t([3, 4, 5])

    oset3 = oset1 & oset2
    assertEqual(oset3, set_t([3]))

    oset4 = oset1.copy()
    oset4 &= oset2

    assertEqual(oset4, oset3)

    oset5 = oset1.copy()
    oset5.intersection_update(oset2)
    assertEqual(oset5, oset3)


@pytest.mark.parametrize("set_t", all_sets)
def test_issubset(set_t):
    oset1 = set_t([1, 2, 3])
    oset2 = set_t([1, 2])

    assertTrue(oset2 < oset1)
    assertTrue(oset2.issubset(oset1))

    oset2 = set_t([1, 2, 3])
    assertTrue(oset2 <= oset1)
    assertTrue(oset1 <= oset2)
    assertTrue(oset2.issubset(oset1))

    oset2 = set_t([1, 2, 3, 4])
    assertFalse(oset2 < oset1)
    assertFalse(oset2.issubset(oset1))
    assertTrue(oset1 < oset2)

    # issubset compares unordered for all sets
    oset2 = set_t([4, 3, 2, 1])
    assertTrue(oset1 < oset2)


@pytest.mark.parametrize("set_t", all_sets)
def test_issuperset(set_t):
    oset1 = set_t([1, 2, 3])
    oset2 = set_t([1, 2])

    assertTrue(oset1 > oset2)
    assertTrue(oset1.issuperset(oset2))

    oset2 = set_t([1, 2, 3])
    assertTrue(oset1 >= oset2)
    assertTrue(oset2 >= oset1)
    assertTrue(oset1.issubset(oset2))

    oset2 = set_t([1, 2, 3, 4])
    assertFalse(oset1 > oset2)
    assertFalse(oset1.issuperset(oset2))
    assertTrue(oset2 > oset1)

    # issubset compares underordered for all sets
    oset2 = set_t([4, 3, 2, 1])
    assertTrue(oset2 > oset1)


@pytest.mark.parametrize("set_t", all_sets)
def test_symmetric_difference_and_update(set_t):
    oset1 = set_t([1, 2, 3])
    oset2 = set_t([2, 3, 4])

    oset3 = oset1 ^ oset2
    assertEqual(oset3, set_t([1, 4]))

    oset4 = oset1.copy()
    assertEqual(oset4.symmetric_difference(oset2), oset3)

    oset4 ^= oset2
    assertEqual(oset4, oset3)

    oset5 = oset1.copy()
    oset5.symmetric_difference_update(oset2)
    assertEqual(oset5, oset3)


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", stableeq_and_ordered_sets)
def test_union_and_update(set_t, lst: list):
    oset = set_t(lst)
    lst = copy.copy(lst)

    oset2 = oset | [3, 9, 27]
    assertEqual(oset2, lst + [27])

    oset2 = [3, 9, 27] | oset
    assertEqual(oset2, [3, 9, 27, 0, 1, 2, 4, 5, 6, 7, 8])

    # make sure original oset isn't changed
    assertEqual(oset, lst)

    oset1 = set_t(lst)
    oset2 = set_t(lst)

    oset3 = oset1 | oset2
    assertEqual(oset3, oset1)

    assertEqual(oset3, oset1.union(oset2))

    oset1 |= set_t("abc")
    assertEqual(oset1, oset2 | "abc")

    oset1 = set_t(lst)
    oset1.update("abc")
    assertEqual(oset1, oset2 | "abc")


@pytest.mark.parametrize("set_t", stable_and_ordered_sets)
def test_union_with_iterable(set_t):
    oset1 = set_t([1])

    assertEqual(oset1 | [2, 1], set_t([1, 2]))
    oset2 = [2] | oset1
    assertEqual(oset2, set_t([2, 1]))
    oset2 = [1, 2] | set_t([3, 1, 2, 4])
    assertEqual(oset2, set_t([1, 2, 3, 4]))

    # union with unordered set should work, though the order will be arbitrary
    oset2 = oset1 | set([2])
    assertEqual(oset2, set_t([1, 2]))
    oset2 = set([2]) | oset1
    assertEqual(oset2, set_t([2, 1]))


@pytest.mark.parametrize("set_t", stable_and_ordered_sets)
def test_symmetric_difference_with_iterable(set_t):
    oset1 = set_t([1])

    assertEqual(oset1 ^ [1], set_t([]))
    assertEqual([1] ^ oset1, set_t([]))

    assertEqual(set_t([3, 1, 4, 2]) ^ [3, 4], set_t([1, 2]))
    assertEqual([3, 1, 4, 2] ^ set_t([3, 4]), set_t([1, 2]))

    assertEqual(set_t([3, 1, 4, 2]) ^ set([3, 4]), set_t([1, 2]))
    oset2 = set([3, 1, 4]) ^ set_t([3, 4, 2])
    assertEqual(oset2, set_t([1, 2]))


@pytest.mark.parametrize("set_t", stable_and_ordered_sets)
def test_intersection_with_iterable(set_t):
    assertEqual([1, 2, 3] & set_t([3, 2]), set_t([2, 3]))
    assertEqual(set_t([3, 2] & set_t([1, 2, 3])), set_t([3, 2]))


@pytest.mark.parametrize("set_t", stable_and_ordered_sets)
def test_difference_with_iterable(set_t):
    assertEqual(set_t([1, 2, 3, 4]) - [3, 2], set_t([1, 4]))
    assertEqual([3, 2, 4, 1] - set_t([2, 4]), set_t([3, 1]))


@pytest.mark.parametrize("set_t", all_sets)
def test_isdisjoint(set_t):
    assertTrue(set_t().isdisjoint(set_t()))
    assertTrue(set_t([1]).isdisjoint(set_t([2])))
    assertFalse(set_t([1, 2]).isdisjoint(set_t([2, 3])))


@pytest.mark.parametrize("set_t", stable_and_ordered_sets)
def test_index(set_t):
    oset = set_t("abcd")
    assertEqual(oset.index("b"), 1)


@pytest.mark.parametrize("set_t", stable_and_ordered_sets)
def test_getitem(set_t):
    oset = set_t("abcd")
    assertEqual(oset[2], "c")


@pytest.mark.parametrize("set_t", stable_and_ordered_sets)
def test_getitem_slice(set_t):
    oset = set_t("abcdef")
    assertEqual(oset[:2], set_t("ab"))
    assertEqual(oset[2:], set_t("cdef"))
    assertEqual(oset[::-1], set_t("fedcba"))
    assertEqual(oset[1:-1:2], set_t("bd"))
    assertEqual(oset[1::2], set_t("bdf"))


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", all_sets)
def test_len(set_t, lst: list):
    oset = set_t(lst)
    assertEqual(len(oset), len(lst))

    oset.remove(0)
    assertEqual(len(oset), len(lst) - 1)


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", all_sets)
def test_contains(set_t, lst: list):
    oset = set_t(lst)
    assertTrue(1 in oset)


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", stable_and_ordered_sets)
def test_iter_mutated(set_t, lst: list):
    oset = set_t(lst)
    it = iter(oset)
    oset.add("a")

    with pytest.raises(RuntimeError):
        next(it)

    it = reversed(oset)
    oset.add("b")

    with pytest.raises(RuntimeError):
        next(it)


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", all_sets)
def test_iter_and_valid_order(set_t, lst: list):
    oset = set_t(lst)
    assertEqual(list(oset), lst)

    oset = set_t(lst + lst)
    assertEqual(list(oset), lst)


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", stable_and_ordered_sets)
def test_reverse_order(set_t, lst: list):
    oset = set_t(lst)
    assertEqual(list(reversed(oset)), list(reversed(lst)))


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", all_sets)
def test_eq(set_t, lst: list):
    oset1 = set_t(lst)
    oset2 = set_t(lst)

    assertNotEqual(oset1, None)

    assertEqual(oset1, oset2)
    assertEqual(oset1, set(lst))


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", ordered_sets)
def test_eq_list(set_t, lst: list):
    assertEqual(set_t(lst), list(lst))


@pytest.mark.parametrize("set_t", stable_and_ordered_sets)
def test_repr(set_t):
    oset = set_t([1])
    set_class_name = set_t.__name__
    assertEqual(repr(oset), f"{set_class_name}([1])")


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", stable_and_ordered_sets)
def test_subset(set_t, lst: list):
    oset1 = set_t([1, 2, 3])
    oset2 = set_t([1, 2, 3, 4])
    oset3 = set_t([1, 2, 4, 3])
    oset4 = set_t([1, 3, 2, 4])

    assertTrue(oset1.isorderedsubset(oset2))
    assertFalse(oset1.isorderedsubset(oset3))
    assertFalse(oset2.isorderedsubset(oset3))
    assertFalse(oset1.isorderedsubset(oset4))

    assertTrue(oset1 < oset2)
    assertTrue(oset1 < oset3)
    assertFalse(oset2 < oset3)
    assertTrue(oset1 < oset4)


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", stable_and_ordered_sets)
def test_subset_non_consecutive(set_t, lst: list):
    oset1 = set_t([1, 2, 3])
    oset2 = set_t([6, 1, 2, 5, 3, 4])
    oset3 = set_t([6, 1, 2, 5, 4, 3])
    oset4 = set_t([6, 1, 3, 5, 2, 4])

    assertTrue(oset1.isorderedsubset(oset2, non_consecutive=True))
    assertTrue(oset1.isorderedsubset(oset3, non_consecutive=True))
    assertFalse(oset2.isorderedsubset(oset3, non_consecutive=True))
    assertFalse(oset1.isorderedsubset(oset4, non_consecutive=True))

    assertTrue(oset1 < oset2)
    assertTrue(oset1 < oset3)
    assertFalse(oset2 < oset3)
    assertTrue(oset1 < oset4)


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", stable_and_ordered_sets)
def test_superset(set_t, lst: list):
    oset1 = set_t([1, 2, 3])
    oset2 = set_t([1, 2, 3, 4])
    oset3 = set_t([1, 2, 4, 3])
    oset4 = set_t([1, 3, 2, 4])

    assertTrue(oset2.isorderedsuperset(oset1))
    assertFalse(oset3.isorderedsuperset(oset1))
    assertFalse(oset3.isorderedsuperset(oset2))
    assertFalse(oset4.isorderedsuperset(oset1))

    assertTrue(oset2 > oset1)
    assertTrue(oset3 > oset1)
    assertFalse(oset3 > oset2)
    assertTrue(oset4 > oset1)


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", stable_and_ordered_sets)
def test_superset_non_consecutive(set_t, lst: list):
    oset1 = set_t([1, 2, 3])
    oset2 = set_t([6, 1, 2, 5, 3, 4])
    oset3 = set_t([6, 1, 2, 5, 4, 3])
    oset4 = set_t([6, 1, 3, 5, 2, 4])

    assertTrue(oset2.isorderedsuperset(oset1, non_consecutive=True))
    assertTrue(oset3.isorderedsuperset(oset1, non_consecutive=True))
    assertFalse(oset3.isorderedsuperset(oset2, non_consecutive=True))
    assertFalse(oset4.isorderedsuperset(oset1, non_consecutive=True))

    assertTrue(oset2 > oset1)
    assertTrue(oset3 > oset1)
    assertFalse(oset3 > oset2)
    assertTrue(oset4 > oset1)


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", all_sets)
def test_ordering(set_t, lst: list):
    oset1 = set_t(lst)
    oset2 = set_t(lst)

    assertLessEqual(oset2, oset1)
    assertLessEqual(oset2, set(oset1))

    assertGreaterEqual(oset1, oset2)
    assertGreaterEqual(oset1, set(oset2))

    oset3 = set_t(lst[:-1])

    assertLess(oset3, oset1)
    assertLess(oset3, set(oset1))

    assertGreater(oset1, oset3)
    assertGreater(oset1, set(oset3))

    oset4 = set_t(lst[1:])

    assertFalse(oset3 < oset4)
    assertFalse(oset3 < set(oset4))
    assertFalse(oset3 >= oset4)
    assertFalse(oset3 >= set(oset4))
    assertFalse(oset3 < oset4)
    assertFalse(oset3 < set(oset4))
    assertFalse(oset3 >= oset4)
    assertFalse(oset3 >= set(oset4))


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", stableeq_and_ordered_sets)
def test_ordering_with_lists(set_t, lst: list):
    oset1 = set_t(lst)
    oset2 = set_t(lst)

    assertLessEqual(oset2, list(oset1))
    assertGreaterEqual(oset1, list(oset2))

    oset3 = set_t(lst[:-1])

    assertLess(oset3, list(oset1))
    assertGreater(oset1, list(oset3))

    oset4 = set_t(lst[1:])

    assertFalse(oset3 < list(oset4))
    assertFalse(oset3 >= list(oset4))
    assertFalse(oset3 < list(oset4))
    assertFalse(oset3 >= list(oset4))


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", ordered_sets)
def test_eq_reversed_orderedset(set_t, lst: list):
    oset1 = set_t(lst)
    oset2 = set_t(reversed(lst))
    assertNotEqual(oset1, oset2)


@pytest.mark.parametrize("lst", datasets)
@pytest.mark.parametrize("set_t", stableeq_sets)
def test_eq_reversed_stableset(set_t, lst: list):
    oset1 = set_t(lst)
    oset2 = set_t(reversed(lst))
    assertEqual(oset1, oset2)
