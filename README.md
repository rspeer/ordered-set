[![Travis](https://img.shields.io/travis/LuminosoInsight/ordered-set/master.svg?label=Travis%20CI)](https://travis-ci.org/LuminosoInsight/ordered-set)
[![Codecov](https://codecov.io/github/LuminosoInsight/ordered-set/badge.svg?branch=master&service=github)](https://codecov.io/github/LuminosoInsight/ordered-set?branch=master)
[![Pypi](https://img.shields.io/pypi/v/ordered-set.svg)](https://pypi.python.org/pypi/ordered-set)

An OrderedSet is a custom MutableSet that remembers its order, so that every
entry has an index that can be looked up.

## Usage examples

An OrderedSet is created and used like a set:

    >>> from ordered_set import OrderedSet

    >>> letters = OrderedSet('abracadabra')

    >>> letters
    OrderedSet(['a', 'b', 'r', 'c', 'd'])

    >>> 'r' in letters
    True

It is efficient to find the index of an entry in an OrderedSet, or find an
entry by its index. To help with this use case, the `.add()` method returns
the index of the added item, whether it was already in the set or not.

    >>> letters.index('r')
    2

    >>> letters[2]
    'r'

    >>> letters.add('r')
    2

    >>> letters.add('x')
    5

OrderedSets implement the union (`|`), intersection (`&`), and difference (`-`)
operators like sets do.

    >>> letters |= OrderedSet('shazam')

    >>> letters
    OrderedSet(['a', 'b', 'r', 'c', 'd', 'x', 's', 'h', 'z', 'm'])

    >>> letters & set('aeiou')
    OrderedSet(['a'])

    >>> letters -= 'abcd'

    >>> letters
    OrderedSet(['r', 'x', 's', 'h', 'z', 'm'])

The `__getitem__()` and `index()` methods have been extended to accept any
iterable except a string, to perform NumPy-like "fancy indexing".

    >>> letters = OrderedSet('abracadabra')

    >>> letters[[0, 2, 3]]
    OrderedSet(['a', 'r', 'c'])

    >>> letters.index(['a', 'r', 'c'])
    [0, 2, 3]

This combination of features makes OrderedSet a simple implementation of many
of the things that `pandas.Index` is used for. An OrderedSet can be used as a
bi-directional mapping between a sparse vocabulary and dense index numbers.

OrderedSet implements `__getstate__` and `__setstate__` so it can be pickled,
and implements the abstract base classes `collections.MutableSet` and
`collections.Sequence`.


## Authors

OrderedSet was implemented by Rob Speer. Jon Crall contributed changes and
tests to make it fit the Python set API.


## Comparisons

The original implementation of OrderedSet was a [recipe posted to ActiveState
Recipes][recipe] by Raymond Hettiger, released under the MIT license.

[recipe]: http://code.activestate.com/recipes/576694-orderedset/

Hettiger's implementation kept its content in a doubly-linked list referenced by a
dict. As a result, looking up an item by its index was an O(N) operation, while
deletion was O(1).

This version makes different trade-offs for the sake of efficient lookups. Its
content is a standard Python list instead of a doubly-linked list. This
provides O(1) lookups by index at the expense of O(N) deletion, as well as
slightly faster iteration.

If you were to use a Python `dict` as an OrderedSet by ignoring its values, its
lookups and deletions would be similar to Hettiger's implementation, with
iteration speed similar to this implementation.


## Compatibility

OrderedSet is automatically tested on Python 2.7, 3.3, 3.4, 3.5, 3.6, and 3.7.
We've checked more informally that it works on PyPy and PyPy3.
