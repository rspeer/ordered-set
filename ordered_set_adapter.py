# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

minghu6:

    Class OrderedSetAdapter can operate with Python set and return Python set.
    This class operates as supplements to the OrderedSet (modified by mine)
    
"""
from ordered_set import OrderedSet

def _acquire_set(f):

    def wrapper(this, other):

        if not isinstance(other,(OrderedSetAdapter, set)):
            raise TypeError(('both of operation object are expected '
                             'OrderedSetAdapter or Python set'))
        else:
            return f(this, other)

    return wrapper


class OrderedSetAdapter(OrderedSet):

    @_acquire_set
    def __eq__(self, other):
        return set(self) == set(other)

    @_acquire_set
    def __gt__(self, other):
        return set(self) > set(other)


    @_acquire_set
    def __lt__(self, other):
        return set(self) < set(other)

    @_acquire_set
    def __ge__(self, other):
        return set(self) >= set(other)

    @_acquire_set
    def __le__(self, other):
        return set(self) <= set(other)

    def issubset(self, other):
        return self.__le__(other)

    def issuperset(self, other):
        return self.__ge__(other)

    @_acquire_set
    def __and__(self, other):
        return set(self) & set(other)

    def __iand__(self, other):
        self = OrderedSetAdapter(self.__and__(other))
        return self

    def intersection(self, other):
        return self.__and__(other)

    def intersection_update(self, other):
        self = OrderedSetAdapter(self.__and__(other))
        return self

    def isdisjoint(self, other):
        if len(self.intersection(other)) == 0:
            return True
        else:
            return False

    @_acquire_set
    def __or__(self, other):
        return set(self).union(set(other))

    @_acquire_set
    def __sub__(self, other):
        return set(self) - set(other)

    def __isub__(self, other):
        self = OrderedSetAdapter(self.__sub__(other))
        return self

    def diffrence(self, other):
        return self.__sub__(other)

    def diffrence_update(self, other):
        self = OrderedSetAdapter(self.__sub__(other))
        return self

    def __ior__(self, other):
        self = OrderedSetAdapter(self.__or__(other))
        return self

    def __rand__(self, other):
        return self.__and__(other)

    def __ror__(self, other):
        return self.__or__(other)

    @_acquire_set
    def __xor__(self, other):
        return set(self) ^ set(other)

    def __ixor__(self, other):
        self = OrderedSetAdapter(set(self) ^ set(other))
        return self

    @_acquire_set
    def __rxor__(self, other):
        return set(other) | set(self)

    def __ne__(self, other):
        return not self.__eq__(other)

    def symmetric_difference(self, other):
        return self ^ other

    def symmetric_difference_update(self, other):
        self = OrderedSetAdapter(self.__xor__(other))
        return self