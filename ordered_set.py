"""
An OrderedSet is a custom MutableSet that remembers its order, so that every
entry has an index that can be looked up. It can also act like a Sequence.

Based on a recipe originally posted to ActiveState Recipes by Raymond Hettiger,
and released under the MIT license.
"""
import itertools as it
from abc import ABC, abstractmethod
from typing import (
    AbstractSet,
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    MutableSet,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    Union,
    overload,
)

SLICE_ALL = slice(None)
__version__ = "4.0"


T = TypeVar("T")
SetLike = Union[Sequence[T], Set[T]]


def _is_atomic(obj: Any) -> bool:
    """
    Returns True for objects which are iterable but should not be iterated in
    the context of indexing an OrderedSet.

    When we index by an iterable, usually that means we're being asked to look
    up a list of things.

    However, in the case of the .index() method, we shouldn't handle strings
    and tuples like other iterables. They're not sequences of things to look
    up, they're the single, atomic thing we're trying to find.

    As an example, oset.index('hello') should give the index of 'hello' in an
    OrderedSet of strings. It shouldn't give the indexes of each individual
    character.
    """
    return isinstance(obj, str) or isinstance(obj, tuple)


class _AbstractOrderedSet(ABC, AbstractSet[T], Sequence[T]):
    """Common functionality shared between OrderedSet and FrozenOrderedSet."""

    @property
    @abstractmethod
    def _items(self) -> Sequence[T]:
        """This stores the de-duplicated elements in order."""
        pass

    @property
    @abstractmethod
    def _map(self) -> Dict[T, int]:
        """This maps the elements to their index for O(1) time complexity with .index() and
        __contains__()."""
        pass

    def __len__(self) -> int:
        return len(self._items)

    def copy(self):
        return self.__class__(self)

    def __getitem__(self, index: int):
        if isinstance(index, slice) and index == SLICE_ALL:
            return self.copy()
        if isinstance(index, Iterable):
            return [self._items[i] for i in index]
        if isinstance(index, slice) or hasattr(index, "__index__"):
            result = self._items[index]
            if isinstance(result, list):
                return self.__class__(result)
            return result
        raise TypeError("Don't know how to index an OrderedSet by %r" % index)

    def __contains__(self, key: Any) -> bool:
        return key in self._map

    def index(self, key: Sequence[T]) -> List[int]:
        if isinstance(key, Iterable) and not _is_atomic(key):
            return [self.index(subkey) for subkey in key]
        return self._map[key]

    # Provide some compatibility with pd.Index
    get_loc = index
    get_indexer = index

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __reversed__(self) -> Iterator[T]:
        return reversed(self._items)

    def __repr__(self) -> str:
        if not self:
            return "%s()" % (self.__class__.__name__,)
        return "%s(%r)" % (self.__class__.__name__, list(self))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Sequence):
            # Check that this OrderedSet contains the same elements, in the
            # same order, as the other object.
            return list(self) == list(other)
        try:
            other_as_set = set(other)
        except TypeError:
            # If `other` can't be converted into a set, it's not equal.
            return False
        else:
            return set(self) == other_as_set

    def union(self, *sets: SetLike[T]):
        cls = self.__class__
        containers = map(list, it.chain([self], sets))
        items = it.chain.from_iterable(containers)
        return cls(items)

    def __and__(self, other: SetLike[T]):
        # the parent implementation of this is backwards
        return self.intersection(other)

    def intersection(self, *sets: SetLike[T]):
        cls = self.__class__
        if not sets:
            return cls(self)
        common = set.intersection(*map(set, sets))
        return cls(item for item in self if item in common)

    def difference(self, *sets: SetLike[T]):
        cls = self.__class__
        if not sets:
            return cls(self)
        other = set.union(*map(set, sets))
        return cls(item for item in self if item not in other)

    def issubset(self, other: SetLike[T]) -> bool:
        if len(self) > len(other):  # Fast check for obvious cases
            return False
        return all(item in other for item in self)

    def issuperset(self, other: SetLike[T]) -> bool:
        if self is None or other is None:
            import pdb; pdb.set_trace()
        if len(self) < len(other):  # Fast check for obvious cases
            return False
        return all(item in self for item in other)

    def symmetric_difference(self, other: SetLike[T]):
        cls = self.__class__
        diff1 = cls(self).difference(other)
        diff2 = cls(other).difference(self)
        return diff1.union(diff2)


class OrderedSet(_AbstractOrderedSet[T], MutableSet[T]):
    """
    An OrderedSet is a custom MutableSet that remembers its order, so that
    every entry has an index that can be looked up.

    Example:
        >>> OrderedSet([1, 1, 2, 3, 2])
        OrderedSet([1, 2, 3])
    """

    def __init__(self, iterable: Optional[Iterable[T]] = None):
        self._items_buffer = []  # type: List[T]
        self._map_buffer = {}  # type: Dict[T, int]
        if iterable is not None:
            self |= iterable

    @property
    def _items(self) -> List[T]:
        return self._items_buffer

    @_items.setter
    def items(self, new_items: List[T]) -> None:
        self._items_buffer = new_items

    @property
    def _map(self) -> Dict[T, int]:
        return self._map_buffer

    @_map.setter
    def map(self, new_map: Dict[T, int]) -> None:
        self._map_buffer = new_map

    def __len__(self) -> int:
        """
        Returns the number of unique elements in the ordered set

        Example:
            >>> len(OrderedSet([]))
            0
            >>> len(OrderedSet([1, 2]))
            2
        """
        return super().__len__()

    @overload
    def __getitem__(self, index: Sequence[int]) -> List[T]:
        ...

    @overload
    def __getitem__(self, index: slice) -> "OrderedSet[T]":
        ...

    def __getitem__(self, index: int) -> T:
        """
        Get the item at a given index.

        If `index` is a slice, you will get back that slice of items, as a
        new OrderedSet.

        If `index` is a list or a similar iterable, you'll get a list of
        items corresponding to those indices. This is similar to NumPy's
        "fancy indexing". The result is not an OrderedSet because you may ask
        for duplicate indices, and the number of elements returned should be
        the number of elements asked for.

        Example:
            >>> oset = OrderedSet([1, 2, 3])
            >>> oset[1]
            2
        """
        return super().__getitem__(index)

    def copy(self) -> "OrderedSet[T]":
        """
        Return a shallow copy of this object.

        Example:
            >>> this = OrderedSet([1, 2, 3])
            >>> other = this.copy()
            >>> this == other
            True
            >>> this is other
            False
        """
        return super().copy()

    def __contains__(self, key: Any) -> bool:
        """
        Test if the item is in this ordered set.

        Example:
            >>> 1 in OrderedSet([1, 3, 2])
            True
            >>> 5 in OrderedSet([1, 3, 2])
            False
        """
        return super().__contains__(key)

    @overload
    def index(self, key: T) -> int:
        ...

    def index(self, key: Sequence[T]) -> List[int]:
        """
        Get the index of a given entry, raising an IndexError if it's not
        present.

        `key` can be an iterable of entries that is not a string, in which case
        this returns a list of indices.

        Example:
            >>> oset = OrderedSet([1, 2, 3])
            >>> oset.index(2)
            1
        """
        return super().index(key)

    def __iter__(self) -> Iterator[T]:
        """
        Example:
            >>> list(iter(OrderedSet([1, 2, 3])))
            [1, 2, 3]
        """
        return super().__iter__()

    def __reversed__(self) -> Iterator[T]:
        """
        Example:
            >>> list(reversed(OrderedSet([1, 2, 3])))
            [3, 2, 1]
        """
        return super().__reversed__()

    def __eq__(self, other: Any) -> bool:
        """
        Returns true if the containers have the same items. If `other` is a
        Sequence, then order is checked, otherwise it is ignored.

        Example:
            >>> oset = OrderedSet([1, 3, 2])
            >>> oset == [1, 3, 2]
            True
            >>> oset == [1, 2, 3]
            False
            >>> oset == [2, 3]
            False
            >>> oset == OrderedSet([3, 2, 1])
            False
        """
        return super().__eq__(other)

    def union(self, *sets: SetLike[T]) -> "OrderedSet[T]":
        """
        Combines all unique items.
        Each items order is defined by its first appearance.

        Example:
            >>> oset = OrderedSet([3, 1, 4, 1, 5]).union([1, 3], [2, 0])
            >>> print(oset)
            OrderedSet([3, 1, 4, 5, 2, 0])
            >>> oset.union([8, 9])
            OrderedSet([3, 1, 4, 5, 2, 0, 8, 9])
            >>> oset | {10}
            OrderedSet([3, 1, 4, 5, 2, 0, 10])
        """
        return super().union(*sets)

    def __and__(self, other: SetLike[T]) -> "OrderedSet[T]":
        # the parent implementation of this is backwards
        return super().__and__(other)

    def intersection(self, *sets: SetLike[T]) -> "OrderedSet[T]":
        """
        Returns elements in common between all sets. Order is defined only
        by the first set.

        Example:
            >>> oset = OrderedSet([0, 1, 2, 3]).intersection([1, 2, 3])
            >>> print(oset)
            OrderedSet([1, 2, 3])
            >>> oset.intersection([2, 4, 5], [1, 2, 3, 4])
            OrderedSet([2])
            >>> oset.intersection()
            OrderedSet([1, 2, 3])
        """
        return super().intersection(*sets)

    def difference(self, *sets: SetLike[T]) -> "OrderedSet[T]":
        """
        Returns all elements that are in this set but not the others.

        Example:
            >>> OrderedSet([1, 2, 3]).difference([2])
            OrderedSet([1, 3])
            >>> OrderedSet([1, 2, 3]).difference([2], [3])
            OrderedSet([1])
            >>> OrderedSet([1, 2, 3]) - [2]
            OrderedSet([1, 3])
            >>> OrderedSet([1, 2, 3]).difference()
            OrderedSet([1, 2, 3])
        """
        return super().difference(*sets)

    def issubset(self, other: SetLike[T]) -> bool:
        """
        Report whether another set contains this set.

        Example:
            >>> OrderedSet([1, 2, 3]).issubset({1, 2})
            False
            >>> OrderedSet([1, 2, 3]).issubset({1, 2, 3, 4})
            True
            >>> OrderedSet([1, 2, 3]).issubset({1, 4, 3, 5})
            False
        """
        return super().issubset(other)

    def issuperset(self, other: SetLike[T]) -> bool:
        """
        Report whether this set contains another set.

        Example:
            >>> OrderedSet([1, 2]).issuperset([1, 2, 3])
            False
            >>> OrderedSet([1, 2, 3, 4]).issuperset({1, 2, 3})
            True
            >>> OrderedSet([1, 4, 3, 5]).issuperset({1, 2, 3})
            False
        """
        return super().issuperset(other)

    def symmetric_difference(self, other: SetLike[T]) -> "OrderedSet[T]":
        """
        Return the symmetric difference of this OrderedSet with another set as a new
        OrderedSet. That is, the new set will contain all elements that are in exactly
        one of the sets.

        Their order will be preserved, with elements from `self` preceding
        elements from `other`.

        Example:
            >>> this = OrderedSet([1, 4, 3, 5, 7])
            >>> other = OrderedSet([9, 7, 1, 3, 2])
            >>> this.symmetric_difference(other)
            OrderedSet([4, 5, 9, 2])
        """
        return super().symmetric_difference(other)

    # Define the gritty details of how an OrderedSet is serialized as a pickle.
    # We leave off type annotations, because the only code that should interact
    # with these is a generalized tool such as pickle.
    def __getstate__(self):
        if len(self) == 0:
            # In pickle, the state can't be an empty list.
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

    def add(self, key: T) -> int:
        """
        Add `key` as an item to this OrderedSet, then return its index.

        If `key` is already in the OrderedSet, return the index it already
        had.

        Example:
            >>> oset = OrderedSet()
            >>> oset.append(3)
            0
            >>> print(oset)
            OrderedSet([3])
        """
        if key not in self._map:
            self._map[key] = len(self._items)
            self._items.append(key)
        return self._map[key]

    append = add

    def update(self, sequence: SetLike[T]) -> int:
        """
        Update the set with the given iterable sequence, then return the index
        of the last element inserted.

        Example:
            >>> oset = OrderedSet([1, 2, 3])
            >>> oset.update([3, 1, 5, 1, 4])
            4
            >>> print(oset)
            OrderedSet([1, 2, 3, 5, 4])
        """
        item_index = 0
        try:
            for item in sequence:
                item_index = self.add(item)
        except TypeError:
            raise ValueError(
                "Argument needs to be an iterable, got %s" % type(sequence)
            )
        return item_index

    def pop(self) -> T:
        """
        Remove and return the last element from the set.

        Raises KeyError if the set is empty.

        Example:
            >>> oset = OrderedSet([1, 2, 3])
            >>> oset.pop()
            3
        """
        if not self._items:
            raise KeyError("Set is empty")

        elem = self._items[-1]
        del self._items[-1]
        del self._map[elem]
        return elem

    def discard(self, key: T) -> None:
        """
        Remove an element.  Do not raise an exception if absent.

        The MutableSet mixin uses this to implement the .remove() method, which
        *does* raise an error when asked to remove a non-existent item.

        Example:
            >>> oset = OrderedSet([1, 2, 3])
            >>> oset.discard(2)
            >>> print(oset)
            OrderedSet([1, 3])
            >>> oset.discard(2)
            >>> print(oset)
            OrderedSet([1, 3])
        """
        if key in self:
            i = self._map[key]
            del self._items[i]
            del self._map[key]
            for k, v in self._map.items():
                if v >= i:
                    self._map[k] = v - 1

    def clear(self) -> None:
        """
        Remove all items from this OrderedSet.
        """
        del self._items[:]
        self._map.clear()

    def _update_items(self, items: list) -> None:
        """
        Replace the 'items' list of this OrderedSet with a new one, updating
        self.map accordingly.
        """
        self.items = items
        self.map = {item: idx for (idx, item) in enumerate(items)}

    def difference_update(self, *sets: SetLike[T]) -> None:
        """
        Update this OrderedSet to remove items from one or more other sets.

        Example:
            >>> this = OrderedSet([1, 2, 3])
            >>> this.difference_update(OrderedSet([2, 4]))
            >>> print(this)
            OrderedSet([1, 3])

            >>> this = OrderedSet([1, 2, 3, 4, 5])
            >>> this.difference_update(OrderedSet([2, 4]), OrderedSet([1, 4, 6]))
            >>> print(this)
            OrderedSet([3, 5])
        """
        items_to_remove = set()  # type: Set[T]
        for other in sets:
            items_as_set = set(other)  # type: Set[T]
            items_to_remove |= items_as_set
        self._update_items([item for item in self._items if item not in items_to_remove])

    def intersection_update(self, other: SetLike[T]) -> None:
        """
        Update this OrderedSet to keep only items in another set, preserving
        their order in this set.

        Example:
            >>> this = OrderedSet([1, 4, 3, 5, 7])
            >>> other = OrderedSet([9, 7, 1, 3, 2])
            >>> this.intersection_update(other)
            >>> print(this)
            OrderedSet([1, 3, 7])
        """
        other = set(other)
        self._update_items([item for item in self._items if item in other])

    def symmetric_difference_update(self, other: SetLike[T]) -> None:
        """
        Update this OrderedSet to remove items from another set, then
        add items from the other set that were not present in this set.

        Example:
            >>> this = OrderedSet([1, 4, 3, 5, 7])
            >>> other = OrderedSet([9, 7, 1, 3, 2])
            >>> this.symmetric_difference_update(other)
            >>> print(this)
            OrderedSet([4, 5, 9, 2])
        """
        items_to_add = [item for item in other if item not in self]
        items_to_remove = set(other)
        self._update_items(
            [item for item in self._items if item not in items_to_remove] + items_to_add
        )


class FrozenOrderedSet(_AbstractOrderedSet[T]):
    """
    A FrozenOrderedSet is a custom AbstractSet that remembers its order, so that
    every entry has an index that can be looked up.

    Example:
        >>> FrozenOrderedSet([1, 1, 2, 3, 2])
        FrozenOrderedSet([1, 2, 3])
    """

    def __init__(self, iterable: Optional[Iterable[T]] = None):
        self._items_buffer = tuple(OrderedSet(iterable))  # type: Tuple[T, ...]
        self._map_buffer = {v: i for i, v in enumerate(self._items)}  # type: Dict[T, int]

    @property
    def _items(self) -> Tuple[T, ...]:
        return self._items_buffer

    @property
    def _map(self) -> Dict[T, int]:
        return self._map_buffer

    def __len__(self):
        """
        Returns the number of unique elements in the ordered set.

        Example:
            >>> len(FrozenOrderedSet([]))
            0
            >>> len(FrozenOrderedSet([1, 2]))
            2
        """
        return super().__len__()

    @overload
    def __getitem__(self, index: Sequence[int]) -> List[T]:
        ...

    @overload
    def __getitem__(self, index: slice) -> "FrozenOrderedSet[T]":
        ...

    def __getitem__(self, index: int) -> T:
        """
        Get the item at a given index.

        If `index` is a slice, you will get back that slice of items, as a
        new OrderedSet.

        If `index` is a list or a similar iterable, you'll get a list of
        items corresponding to those indices. This is similar to NumPy's
        "fancy indexing". The result is not an OrderedSet because you may ask
        for duplicate indices, and the number of elements returned should be
        the number of elements asked for.

        Example:
            >>> fo_set = FrozenOrderedSet([1, 2, 3])
            >>> fo_set[1]
            2
        """
        return super().__getitem__(index)

    def copy(self) -> "FrozenOrderedSet[T]":
        """
        Return a shallow copy of this object.

        Example:
            >>> this = FrozenOrderedSet([1, 2, 3])
            >>> other = this.copy()
            >>> this == other
            True
            >>> this is other
            False
        """
        return super().copy()

    def __contains__(self, key: Any) -> bool:
        """
        Test if the item is in this ordered set.

        Example:
            >>> 1 in FrozenOrderedSet([1, 3, 2])
            True
            >>> 5 in FrozenOrderedSet([1, 3, 2])
            False
        """
        return super().__contains__(key)

    @overload
    def index(self, key: T) -> int:
        ...

    def index(self, key: Sequence[T]) -> List[int]:
        """
        Get the index of a given entry, raising an IndexError if it's not
        present.

        `key` can be an iterable of entries that is not a string, in which case
        this returns a list of indices.

        Example:
            >>> fo_set = FrozenOrderedSet([1, 2, 3])
            >>> fo_set.index(2)
            1
        """
        return super().index(key)

    def __iter__(self) -> Iterator[T]:
        """
        Example:
            >>> list(iter(FrozenOrderedSet([1, 2, 3])))
            [1, 2, 3]
        """
        return super().__iter__()

    def __reversed__(self) -> Iterator[T]:
        """
        Example:
            >>> list(reversed(FrozenOrderedSet([1, 2, 3])))
            [3, 2, 1]
        """
        return super().__reversed__()

    def __eq__(self, other: Any) -> bool:
        """
        Returns true if the containers have the same items. If `other` is a
        Sequence, then order is checked, otherwise it is ignored.

        Example:
            >>> fo_set = FrozenOrderedSet([1, 3, 2])
            >>> fo_set == [1, 3, 2]
            True
            >>> fo_set == [1, 2, 3]
            False
            >>> fo_set == [2, 3]
            False
            >>> fo_set == FrozenOrderedSet([3, 2, 1])
            False
        """
        return super().__eq__(other)

    def __hash__(self) -> int:
        return hash(self._items)

    def union(self, *sets: SetLike[T]) -> "FrozenOrderedSet[T]":
        """
        Combines all unique items.
        Each items order is defined by its first appearance.

        Example:
            >>> fo_set = FrozenOrderedSet([3, 1, 4, 1, 5]).union([1, 3], [2, 0])
            >>> print(fo_set)
            FrozenOrderedSet([3, 1, 4, 5, 2, 0])
            >>> fo_set.union([8, 9])
            FrozenOrderedSet([3, 1, 4, 5, 2, 0, 8, 9])
            >>> fo_set | {10}
            FrozenOrderedSet([3, 1, 4, 5, 2, 0, 10])
        """
        return super().union(*sets)

    def __and__(self, other: SetLike[T]) -> "FrozenOrderedSet[T]":
        # the parent implementation of this is backwards
        return super().__and__(other)

    def intersection(self, *sets: SetLike[T]) -> "FrozenOrderedSet[T]":
        """
        Returns elements in common between all sets. Order is defined only
        by the first set.

        Example:
            >>> fo_set = FrozenOrderedSet([0, 1, 2, 3]).intersection([1, 2, 3])
            >>> print(fo_set)
            FrozenOrderedSet([1, 2, 3])
            >>> fo_set.intersection([2, 4, 5], [1, 2, 3, 4])
            FrozenOrderedSet([2])
            >>> fo_set.intersection()
            FrozenOrderedSet([1, 2, 3])
        """
        return super().intersection(*sets)

    def difference(self, *sets: SetLike[T]) -> "FrozenOrderedSet[T]":
        """
        Returns all elements that are in this set but not the others.

        Example:
            >>> FrozenOrderedSet([1, 2, 3]).difference([2])
            FrozenOrderedSet([1, 3])
            >>> FrozenOrderedSet([1, 2, 3]).difference([2], [3])
            FrozenOrderedSet([1])
            >>> FrozenOrderedSet([1, 2, 3]) - [2]
            FrozenOrderedSet([1, 3])
            >>> FrozenOrderedSet([1, 2, 3]).difference()
            FrozenOrderedSet([1, 2, 3])
        """
        return super().difference(*sets)

    def issubset(self, other: SetLike[T]) -> bool:
        """
        Report whether another set contains this set.

        Example:
            >>> FrozenOrderedSet([1, 2, 3]).issubset({1, 2})
            False
            >>> FrozenOrderedSet([1, 2, 3]).issubset({1, 2, 3, 4})
            True
            >>> FrozenOrderedSet([1, 2, 3]).issubset({1, 4, 3, 5})
            False
        """
        return super().issubset(other)

    def issuperset(self, other: SetLike[T]) -> bool:
        """
        Report whether this set contains another set.

        Example:
            >>> FrozenOrderedSet([1, 2]).issuperset([1, 2, 3])
            False
            >>> FrozenOrderedSet([1, 2, 3, 4]).issuperset({1, 2, 3})
            True
            >>> FrozenOrderedSet([1, 4, 3, 5]).issuperset({1, 2, 3})
            False
        """
        return super().issuperset(other)

    def symmetric_difference(self, other: SetLike[T]) -> "FrozenOrderedSet[T]":
        """
        Return the symmetric difference of this FrozenOrderedSet and another set as a new
        FrozenOrderedSet. That is, the new set will contain all elements that are in
        exactly one of the sets.

        Their order will be preserved, with elements from `self` preceding
        elements from `other`.

        Example:
            >>> this = FrozenOrderedSet([1, 4, 3, 5, 7])
            >>> other = FrozenOrderedSet([9, 7, 1, 3, 2])
            >>> this.symmetric_difference(other)
            FrozenOrderedSet([4, 5, 9, 2])
        """
        return super().symmetric_difference(other)
