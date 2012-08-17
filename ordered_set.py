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

class OrderedSet(collections.MutableSet):
    """
    An OrderedSet is a custom MutableSet that remembers its order, so that
    every entry has an index that can be looked up.
    """
    def __init__(self, iterable=None):
        self.items = []
        self.map = {}
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        if index == SLICE_ALL:
            return self
        elif hasattr(index, '__index__') or isinstance(index, slice):
            result = self.items[index]
            if isinstance(result, list):
                return OrderedSet(result)
            else:
                return result
        elif hasattr(index, '__iter__'):
            return OrderedSet([self.items[i] for i in index])
        else:
            raise TypeError("Don't know how to index an OrderedSet by %r" %
                    index)

    def copy(self):
        return OrderedSet(self)

    def __getstate__(self):
        return list(self)
    
    def __setstate__(self, state):
        self.__init__(state)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            self.map[key] = len(self.items)
            self.items.append(key)
        return self.map[key]
    
    def index(self, key):
        """
        Get the index of a given key, raising an IndexError if it's not
        present.
        """
        if hasattr(key, '__iter__'):
            return [self.index(subkey) for subkey in key]
        return self.map[key]

    def discard(self, key):
        if key in self.map:        
            loc = self.map.pop(key)
            self.items = self.items[:loc] + self.items[loc+1:]

    def __iter__(self):
        return iter(self.items)

    def __reversed__(self):
        return reversed(self.items)

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = next(reversed(self)) if last else next(iter(self))
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and self.items == other.items
        return set(self) == set(other)
            
if __name__ == '__main__':
    import pickle
    print(OrderedSet('abracadaba'))
    test = OrderedSet('simsalabim')
    print(test)
    roundtrip = pickle.loads(pickle.dumps(test))
    print(roundtrip)
    assert (roundtrip == test)
    roundtrip.pop()
    print(roundtrip)
    print(roundtrip[[1, 2]])
    print(roundtrip[:])

