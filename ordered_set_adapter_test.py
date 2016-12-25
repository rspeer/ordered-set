# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from ordered_set_adapter import OrderedSetAdapter

def gt_test():
    set1 = OrderedSetAdapter([3, 5, 2])
    set2 = {3, 5, 2, 1}
    set3 = OrderedSetAdapter([3, 2, 5, 1])

    assert not set1 > set2
    assert set3 > set1


def lt_test():
    set1 = OrderedSetAdapter([3, 5, 2])
    set2 = set([3, 5, 2, 1])
    set3 = OrderedSetAdapter([3, 2, 5, 1, 0])

    assert set1 < set2
    assert set2 < set3

def ge_test():
    set1 = OrderedSetAdapter([3, 5, 2])
    set2 = set([3, 5, 2, 1])
    set3 = OrderedSetAdapter([3, 2, 5, 1])
    set4 = OrderedSetAdapter([3, 5, 2])

    assert set2 >= set1
    assert set3 >= set1
    assert set4 >= set1

def le_test():
    set1 = OrderedSetAdapter([3, 5, 2])
    set2 = OrderedSetAdapter([3, 5, 2, 1])
    set3 = set([3, 2, 5, 1])
    set4 = OrderedSetAdapter([3, 5, 2])

    assert set1 <= set2
    assert set1 <= set3
    assert set1 <= set4

def and_test():
    set1 = OrderedSetAdapter([3, 5, 2])
    set2 = OrderedSetAdapter([3, 5, 2, 1])
    set3 = set([3, 2, 5, 1])
    set4 = OrderedSetAdapter([3, 5, 2])

    assert set2 & set1 == OrderedSetAdapter([3, 5, 2])
    assert set3 & set1 == OrderedSetAdapter([3, 2, 5])
    assert set4 & set1 == OrderedSetAdapter([3, 5, 2])

def symmetric_difference_update_test():
    set1 = OrderedSetAdapter([3, 5, 2])
    set2 = OrderedSetAdapter([3, 5, 2, 1])
    set3 = set([3, 2, 5, 1])
    set4 = set([3, 5, 2])

    assert set1.symmetric_difference_update(set2) == OrderedSetAdapter([1])

def all_i_test():
    set1 = OrderedSetAdapter([3, 5, 2])
    set2 = OrderedSetAdapter([5, 2, 1, 0])

    set1.symmetric_difference(set2)
    set1 -= set2
    set1 |= set2
    set1 &= set2
    set1 ^= set2


def difference_test():
    set1 = OrderedSetAdapter([3, 5, 2])
    set2 = OrderedSetAdapter([5, 1, 0])
    set3 = OrderedSetAdapter([2])

    assert set1.difference(set2, set3) == OrderedSetAdapter([3])

def union_test():
    set1 = OrderedSetAdapter([3,])
    set2 = OrderedSetAdapter([5, 1,])
    set3 = OrderedSetAdapter([2])

    assert set1.union(set2, set3) == OrderedSetAdapter([3, 5, 1, 2])