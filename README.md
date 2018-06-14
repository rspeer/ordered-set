[![Travis](https://img.shields.io/travis/LuminosoInsight/ordered-set/master.svg?label=Travis%20CI)](https://travis-ci.org/LuminosoInsight/ordered-set)
[![Codecov](https://codecov.io/github/LuminosoInsight/ordered-set/badge.svg?branch=master&service=github)](https://codecov.io/github/LuminosoInsight/ordered-set?branch=master)
[![Pypi](https://img.shields.io/pypi/v/ordered-set.svg)](https://pypi.python.org/pypi/ordered-set)


An OrderedSet is a custom MutableSet that remembers its order, so that every
entry has an index that can be looked up.

Based on a recipe originally posted to ActiveState Recipes by Raymond Hettiger,
and released under the MIT license:

    http://code.activestate.com/recipes/576694-orderedset/

This module's changes are as follows:

- Changed the content from a doubly-linked list to a regular Python list.
  The ActiveState version has O(N) lookups by index and O(1) deletion;
  this version has O(1) lookups by index and O(N) deletion, which seems
  more useful in most cases.

- `add()` returns the index of the added item

- `index()` just returns the index of an item

- Added a `__getstate__` and `__setstate__` so it can be pickled

- Added `__getitem__`

- `__getitem__` and `index()` can be passed lists or arrays, looking up
  all the elements in them to perform NumPy-like "fancy indexing"

- The class implements the abstract base classes `collections.MutableSet`
  and `collections.Sequence`

Tested on Python 2.7, 3.3, 3.4, 3.5, PyPy, and PyPy3.
