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
"""
import collections

SLICE_ALL = slice(None)
__version__ = '2.0.1'


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


class OrderedSet(collections.MutableSet, collections.Sequence):
    """
    An OrderedSet is a custom MutableSet that remembers its order, so that
    every entry has an index that can be looked up.
    """
    def __init__(self, iterable=None):
        self.data = collections.OrderedDict()
        if iterable is not None:
            self |= iterable

    #
    # Abstract methods of MutableSet and Sequence
    #
    def __contains__(self, key):
        return key in self.data

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def add(self, key):
        self.data[key] = None
        # OrderedSet specific
        # TODO: Don't know if this was a side effect of the old update implemenation which utilized it
        #       or if it was meant to be a feature used externally.  If the latter, it should have a test added for it
        return self.index(key)

    def discard(self, key):
        if key in self.data:
            del self.data[key]

    def __getitem__(self, index):
        if index == SLICE_ALL:
            return self
        if is_iterable(index):
            return [self[i] for i in index]
        return list(self.data)[index]

    #
    # Other OrderedSet methods
    #
    def update(self, sequence):
        """
        Update the set with the given iterable sequence, then return the index
        of the last element inserted.
        """
        try:
            for item in sequence:
                self.add(item)
        except TypeError:
            raise ValueError('Argument needs to be an iterable, got %s' % type(sequence))
        return self.index(item)

    def pop(self):
        """
        Remove and return the last element from the set.

        Raises KeyError if the set is empty.
        """
        if not self.data:
            raise KeyError('Set is empty')
        elem = next(reversed(self.data))
        del self.data[elem]
        return elem

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and self.data == other.data
        try:
            other_as_set = set(other)
        except TypeError:
            # If `other` can't be converted into a set, it's not equal.
            return False
        else:
            return set(self) == other_as_set

    def copy(self):
        return OrderedSet(self)

    def index(self, key):
        if is_iterable(key):
            return [self.index(k) for k in key]
        try:
            return super(OrderedSet, self).index(key)
        except ValueError:
            raise KeyError
