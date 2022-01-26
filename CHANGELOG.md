# Changelog

Significant changes in major and minor releases of this library:

## Version 4.1 (January 2022)

- Packaged using flit. Wheels now exist, and setuptools is no longer required.
- This package now has a typical package structure, instead of being a single module. The code is in `ordered_set/__init__.py` instead of `ordered_set.py`.
- There is an `ordered_set/py.typed` so that type checkers know about the types.
- Use the type aliases `SetLike[T]` and `OrderedSetInitializer[T]` to simplify some types.
- Updated the way overloaded type signatures are written to what MyPy currently expects.
- Minimum Python version is 3.7.

## Version 4.0 (January 2020)

- Added type signatures inline to the code, instead of using type stubs.
- Dropped Python 2 support. The minimum supported Python version is 3.5.

## Version 3.1 (November 2018)

- `__getitem__` accepts NumPy arrays of indices, and returns a list of elements with those indices.
- Updated in-place operations that took O(N^2) time, such as .difference_update(), to take O(N) time.
- Clarified whether various methods mutate or copy the OrderedSet.
- Added `OrderedSet.get_loc` and `OrderedSet.get_indexer` as aliases for `OrderedSet.index`, for interoperability with `pandas.Index`.
- Added type stubs in a .pyi file.

## Version 3.0 (June 2018)

- Implemented the abstract base classes `collections.MutableSet` and `collections.Sequence`.
- Changed the behavior of some methods to follow the MutableSet API.
- Indexing an OrderedSet with `[:]` returns a copy, not the same object.

## Version 2.0 (December 2015)

- Tuples are allowable values in the set, and are not treated as "fancy indexing".
- Added `update` and `pop` methods.

## Version 1.4 (September 2015)

- Added `discard` and `clear` methods.

## Version 1.3 (April 2015)

- Added support for pickling.

## Version 1.2 (May 2014)

- First Python 3 support.

## Version 1.1 (August 2013)

- Added tests.
- Removed a broken implementation of `discard`.

## Version 1.0 (August 2012)

- First release.
