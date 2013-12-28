import math
import random

from numpy.random import geometric

import collections.abc as colabc


__all__ = ('SkipListDict', 'SkipListDictDefault', 'SkipListSet')
#===============================================================================
# TODO:
# - why math.e
# - need double direction and reverse?
#===============================================================================


class SkipListDict(colabc.MutableMapping):
    """
    keys only need __lt__ operation
    """
    def __init__(self, capacity=65535, p=1 / math.e):
        self._max_level = int(math.log(capacity, 2))
        self._level = 0
        self._head = self._make_node(self._max_level, None, None)
        self._nil = self._make_node(-1, None, None)
        self._tail = self._nil
        self._head[3:] = [self._nil for _ in range(1 + self._max_level)]  # fixed +1
        self._update = [self._head] * (1 + self._max_level)
        self._p = p
        self._size = 0
        self._capacity = capacity
        self._last_getitem = None  # will be set to (node, update) by setdefault

    @property
    def capacity(self):
        return self._capacity

    def _make_node(self, level, key, value):
        node = [None] * (4 + level)
        node[0] = key
        node[1] = value
        return node

    def _random_level(self):
        lvl = 0
        max_level = min(self._max_level, self._level + 1)
        while random.random() < self._p and lvl < max_level:
            lvl += 1
        return lvl

#     def _random_level(self):
#         lvl = geometric(self._p)
#         return (lvl if lvl <= self._level else
#                 self._level + 1 if self._level + 1 < self._max_level else
#                 self._max_level)
#         return lvl

    def pop(self):
        if self._size < 1:
            raise KeyError("Cannot pop() from empty skiplist")

        update = self._update[:]
        node = self._head
        node = node[3]

        key, value = node[:2]

        node[3][2] = update[0]

        for i in range(self._level + 1):
            if update[i][3 + i] is not node:
                break

            update[i][3 + i] = node[3 + i]

        while self._level > 0 and self._head[3 + self._level][0] is None:
            self._level -= 1

        if self._tail is node:
            self._tail = node[2]

        self._size -= 1

        return key, value

    def items(self, start_key=None, reverse=False):
        if reverse:
            node = self._tail
        else:
            node = self._head[3]
        if start_key is not None:
            update = self._update[:]
            found = self._find_less(update, start_key)
            # if found[3] is not self._nil: # OTHERWISE keys beyond largest yield full list
            node = found[3]
        idx = 2 if reverse else 3
        while node[0] is not None:
            yield node[0], node[1]
            node = node[idx]

    def keys(self, start_key=None, reverse=False):
        for k, _v in self.items(start_key, reverse):
            yield k

    def values(self, start_key=None, reverse=False):
        for _k, v in self.items(start_key, reverse):
            yield v

    def _find_less(self, update, key):
        node = self._head
        for i in range(self._level, -1, -1):
            current_key = node[3 + i][0]
            while current_key is not None and current_key < key:  # Key comparison
                node = node[3 + i]
                current_key = node[3 + i][0]
            update[i] = node
        return node

    def __len__(self):
        return self._size

    def __setitem__(self, key, value):
        assert key is not None
        update = self._update[:]
        node = self._find_less(update, key)
        prev = node
        node = node[3]

        if node[0] == key:
            node[1] = value
        else:
            lvl = self._random_level()
            if lvl > self._level:
                self._level = lvl
            node = self._make_node(lvl, key, value)
            node[2] = prev

            for i in range(0, lvl + 1):
                node[3 + i] = update[i][3 + i]
                update[i][3 + i] = node

            if node[3] is self._nil:
                self._tail = node
            else:
                node[3][2] = node

            self._size += 1

    def setdefault(self, key, default):
        assert key is not None
        update = self._update[:]
        node = self._find_less(update, key)
        prev = node
        node = node[3]

        if node[0] != key:
            lvl = self._random_level()
            if lvl > self._level:
                self._level = lvl
            node = self._make_node(lvl, key, default)
            node[2] = prev

            for i in range(0, lvl + 1):
                node[3 + i] = update[i][3 + i]  # bug
                update[i][3 + i] = node

            if node[3] is self._nil:
                self._tail = node
            else:
                node[3][2] = node

            self._size += 1
        self._last_getitem = (node, update)
        return node[1]

    def __delitem__(self, key):
        update = self._update[:]
        node = self._find_less(update, key)
        node = node[3]

        if node[0] == key:
            node[3][2] = update[0]

            for i in range(self._level + 1):
                if update[i][3 + i] is not node:
                    break

                update[i][3 + i] = node[3 + i]

            while self._level > 0 and self._head[3 + self._level][0] is None:
                self._level -= 1

            if self._tail is node:
                self._tail = node[2]

            self._size -= 1
        else:
            raise KeyError('Key {} not found'.format(key))

    def __getitem__(self, key):
        node = self._head

        for i in range(self._level, -1, -1):
            current_key = node[3 + i][0]

            while current_key is not None and current_key < key:  # Key comparison
                node = node[3 + i]
                current_key = node[3 + i][0]

        node = node[3]

        if node[0] == key:
            return node[1]
        else:
            raise KeyError('Key {} not found'.format(key))

    def __iter__(self):
        for k, _v in self.items():
            yield k

    def __repr__(self):
        return '{0.__class__.__name__}({1}, capacity={0._capacity})'.format(
            self,
            '{' + ', '.join('{0!r}: {1!r}'.format(k, v) for (k, v) in self.items()) + '}')


class SkipListSet(colabc.MutableSet):
    def __init__(self, capacity):
        self._storage = SkipListDict(capacity=capacity)

    def __contains__(self, key):
        return key in self._storage

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)
        pass

    def add(self, key):
        self._storage[key] = None

    def discard(self, key):
        del self._storage[key]

    def __repr__(self):
        return '{0.__class__.__name__}({1!r}, capacity={0._storage.capacity})'.format(
            self, tuple(self))


class SkipListDictDefault(SkipListDict):
    def __init__(self, default_class, **kwargs):
        SkipListDict.__init__(self, **kwargs)
        self._default_class = default_class

    def __getitem__(self, key):
        return self.setdefault(key, self._default_class())

    def remove_empty_last(self):
        node, update = self._last_getitem
        if not node[1]:
            node[3][2] = update[0]

            for i in range(self._level + 1):
                if update[i][3 + i] is not node:
                    break

                update[i][3 + i] = node[3 + i]

            while self._level > 0 and self._head[3 + self._level][0] is None:
                self._level -= 1

            if self._tail is node:
                self._tail = node[2]

            self._size -= 1
