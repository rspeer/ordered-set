import timeit
from functools import partial
from random import randint

from ordered_set import OrderedSet as OS2

try:
    from orderedset import OrderedSet as OS1
except ImportError:
    # currently orderedset fails to install on Python 3.10, 3.11
    # https://github.com/simonpercivall/orderedset/issues/36#issuecomment-1424309665
    print("orderedset is not installed, using ordered_set twice")
    OS1 = OS2
from ordered_set import StableSet as OS3
try:
    from sortedcollections import OrderedSet as OS4
except ImportError:
    print("sortedcollections is not installed, using ordered_set twice")
    OS4 = OS2


item_count = 10_000
item_range = item_count * 2
items = [randint(0, item_range) for _ in range(item_count)]
items_b = [randint(0, item_range) for _ in range(item_count)]

oset1a = OS1(items)
oset2a = OS2(items)
oset1b = OS1(items_b)
oset2b = OS2(items_b)
assert oset1a.difference(oset1b) == oset2a.difference(oset2b)
assert oset1a.intersection(oset1b) == oset2a.intersection(oset2b)

oset1c = OS1(items)
oset2c = OS2(items)
oset1c.add(item_range + 1)
oset2c.add(item_range + 1)
assert oset1c == oset2c

for i in range(item_range):
    assert (i in oset1a) == (i in oset2a)
    if i in oset1a:
        assert oset1a.index(i) == oset2a.index(i)


def init_set(T, items) -> set:
    return T(items)


def init_set_list(T, items) -> list:
    return list(T(items))


def init_set_d(items) -> dict:
    return dict.fromkeys(items)


def init_set_d_list(items) -> list:
    return list(dict.fromkeys(items))


def update(s: set, items) -> set:
    s.update(items)
    return s


def update_d(s: dict, items) -> dict:
    d2 = dict.fromkeys(items)
    s.update(d2)
    return s


ordered_sets_types = [OS1, OS2, OS3, OS4]
set_types = [set] + ordered_sets_types

oss = [init_set(T, items) for T in set_types]
od = init_set_d(items)

osls = [init_set_list(T, items) for T in set_types[1:]] + [init_set_d_list(items)]
for x in osls:
    assert osls[0] == x

osls = [update(init_set(T, items), items_b) for T in ordered_sets_types[:-1]] + [
    update_d(init_set_d(items), items_b)
]
osls = [list(x) for x in osls]
for x in osls:
    assert osls[0] == x

number = 10000
repeats = 4
for i in range(repeats):
    print(f"----- {i} ------")

    print("-- init set like --")
    print(f"d: {timeit.timeit(partial(init_set_d, items),number=number)=}")
    for idx, T in enumerate(set_types):
        print(f"{idx}: {timeit.timeit(partial(init_set, T, items),number=number)=}")

    print("-- unique list --")
    print(f"d: {timeit.timeit(partial(init_set_d, items),number=number)=}")
    for idx, T in enumerate(set_types):
        print(
            f"{idx}: {timeit.timeit(partial(init_set_list, T, items),number=number)=}"
        )

    print("-- update set like --")
    print(f"d: {timeit.timeit(partial(update_d, od, items_b),number=number)=}")
    for idx, os in enumerate(oss[:-1]):
        print(f"{idx}: {timeit.timeit(partial(update, os, items_b),number=number)=}")
