"""
An OrderedSet is a custom MutableSet that remembers its order, so that every
entry has an index that can be looked up.

Based on a recipe originally posted to ActiveState Recipes by Raymond Hettiger,
and released under the MIT license.

Rob Speer's changes are as follows:

    - changed the content from a doubly-linked list to a regular Python list.
      Seriously, who wants O(1) deletes but O(N) lookups by index?
    - add() returns the index of the added item
    - index() just returns the index of an item
    - added a __getstate__ and __setstate__ so it can be pickled
    - added __getitem__

minghu6's changes are as follow:

    - restrict the OrderedSet operation object: only themselves
      OrderededSet's element consists of its index and value
      I want to write a new class OrderedSetAdapter
      to adapt Python set

    - rewrite some contradictory method from collections.MutableSet
"""
import collections

SLICE_ALL = slice(None)


def is_iterable(obj):
    """
    Are we being asked to look up a list of things, instead of a single thing?
    We check for the `__iter__` attribute so that this can cover types that
    don't have to be known by this module, such as NumPy arrays.

    Strings, however, should be considered as atomic values to look up, not
    iterables. The same goes for tuples, since they are immutable and therefore
    valid entries.

    We don't need to check for the Python 2 `unicode` type, because it doesn't
    have an `__iter__` attribute anyway.
    """
    return hasattr(obj, '__iter__') and not isinstance(obj, str) and not isinstance(obj, tuple)


def _acquire_ordered_set(f):

    def wrapper(this, other):

        if not isinstance(other, OrderedSet):
            raise TypeError('both of operation object are expected OrderedSet')
        else:
            return f(this, other)

    return wrapper

class UnionError(BaseException):
    def __str__(self):
        return 'two set can not union'

class DifferenceError(BaseException):
    def __str__(self):
        return 'can not compare diffrence of two set'

class SymmetricDifferenceError(BaseException):
    def __str__(self):
        return 'can not get symmetric diffrence of two set'


class OrderedSet(collections.MutableSet):
    """
    An OrderedSet is a custom MutableSet that remembers its order, so that
    every entry has an index that can be looked up.
    """
    def __init__(self, iterable=None):
        self._items = []
        self._map = {}
        if iterable is not None:
            self.update(iterable)

    def get_items(self):
        return self._items.copy()

    items = property(get_items)

    def get_map(self):
        return self._map.copy()

    map = property(get_map)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        """
        Get the item at a given index.

        If `index` is a slice, you will get back that slice of items. If it's
        the slice [:], exactly the same object is returned. (If you want an
        independent copy of an OrderedSet, use `OrderedSet.copy()`.)

        If `index` is an iterable, you'll get the OrderedSet of items
        corresponding to those indices. This is similar to NumPy's
        "fancy indexing".
        """
        if index == SLICE_ALL:
            return self
        elif hasattr(index, '__index__') or isinstance(index, slice):
            result = self._items[index]
            if isinstance(result, list):
                return OrderedSet(result)
            else:
                return result
        elif is_iterable(index):
            return OrderedSet([self._items[i] for i in index])
        else:
            raise TypeError("Don't know how to index an OrderedSet by %r" %
                    index)

    def copy(self):
        return OrderedSet(self)

    def __getstate__(self):
        if len(self) == 0:
            # The state can't be an empty list.
            # We need to return a truthy value, or else __setstate__ won't be run.
            #
            # This could have been done more gracefully by always putting the state
            # in a tuple, but this way is backwards- and forwards- compatible with
            # previous versions of OrderedSet.
            return (None,)
        else:
            return list(self)

    def __setstate__(self, state):
        if state == (None,):
            self.__init__([])
        else:
            self.__init__(state)

    def __contains__(self, key):
        return key in self._map

    def add(self, key):
        """
        Add `key` as an item to this OrderedSet, then return its index.

        If `key` is already in the OrderedSet, return the index it already
        had.
        """
        if key not in self._map:
            self._map[key] = len(self._items)
            self._items.append(key)
        return self._map[key]
    append = add

    def update(self, sequence):
        """
        Update the set with the given iterable sequence, then return the index
        of the last element inserted.
        """
        item_index = None
        try:
            for item in sequence:
                item_index = self.add(item)
        except TypeError:
            raise ValueError('Argument needs to be an iterable, got %s' % type(sequence))
        return item_index

    def index(self, key):
        """
        Get the index of a given entry, raising an IndexError if it's not
        present.

        `key` can be an iterable of entries that is not a string, in which case
        this returns a list of indices.
        """
        if is_iterable(key):
            return [self.index(subkey) for subkey in key]
        return self._map[key]

    def pop(self):
        """
        Remove and return the last element from the set.

        Raises KeyError if the set is empty.
        """
        if not self._items:
            raise KeyError('Set is empty')

        elem = self._items[-1]
        del self._items[-1]
        del self._map[elem]
        return elem

    def discard(self, key):
        """
        Remove an element.  Do not raise an exception if absent.

        The MutableSet mixin uses this to implement the .remove() method, which
        *does* raise an error when asked to remove a non-existent item.
        """
        if key in self:
            i = self._map[key]
            del self._items[i]
            del self._map[key]
            for k, v in self._map.items():
                if v >= i:
                    self._map[k] = v - 1

    def clear(self):
        """
        Remove all items from this OrderedSet.
        """
        del self._items[:]
        self._map.clear()

    def __iter__(self):
        return iter(self._items)

    def __reversed__(self):
        return reversed(self._items)

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and self._items == other._items
        else:
            # OrderedSet cann't compared with set
            return False


    @_acquire_ordered_set
    def __gt__(self, other):

        if len(self._items) <= len(other._items):
            return False
        else:
            for this_item, other_item in zip(self._items, other._items):
                if this_item != other_item:
                    return False

            return True

    @_acquire_ordered_set
    def __lt__(self, other):
        if len(self._items) >= len(other._items):
            return False
        else:
            for this_item, other_item in zip(self._items, other._items):
                if this_item != other_item:
                    return False

            return True

    @_acquire_ordered_set
    def __ge__(self, other):
        if self.__eq__(other) or self.__gt__(other):
            return True
        else:
            return False

    @_acquire_ordered_set
    def __le__(self, other):
        if self.__eq__(other) or self.__lt__(other):
            return True
        else:
            return False

    def issubset(self, other):
        return self.__le__(other)

    def issuperset(self, other):
        return self.__ge__(other)

    @_acquire_ordered_set
    def __and__(self, other):
        res = OrderedSet()
        for this_item, other_item in zip(self._items, other._items):
            if this_item != other_item:
                break
            else:
                res.add(this_item)

        return res

    def intersection(self, *others):
        res = self.__and__(others[0])
        for other in others[1:]:
            res = res.__and__(other)

        return res

    def intersection_update(self, *others):
        res = self.intersection(*others)
        self.clear()
        self.update(res)


    def isdisjoint(self, other):
        if len(self.intersection(other)) == 0:
            return True
        else:
            return False

    @_acquire_ordered_set
    def __or__(self, other):
        if self.issubset(other):
            return other.copy()
        elif self.issuperset(other):
            return self.copy()
        else:
            raise UnionError

    @_acquire_ordered_set
    def __sub__(self, other):
        if self.issubset(other):
            return OrderedSet()
        else:
            raise DifferenceError

    def __iand__(self, other):
        self = self.__and__(other)
        return self

    def __ior__(self, other):
        self = self.__or__(other)
        return self

    def __rand__(self, other):
        return other.__and__(self)

    def __ror__(self, other):
        return other.__or__(self)

    def __xor__(self, other):
        raise SymmetricDifferenceError

    def __ixor__(self, other):
        raise SymmetricDifferenceError

    def __rxor__(self, other):
        raise SymmetricDifferenceError

    def __ne__(self, other):
        return not self.__eq__(other)
