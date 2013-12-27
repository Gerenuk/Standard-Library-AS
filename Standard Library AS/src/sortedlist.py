from skiplist import SkipListDict


class SortedList:
    def __init__(self, sortkey_func):
        self.sortkey_func = sortkey_func
        self._storage = SkipListDict()

    def append(self, value):
        self._storage[self.sortkey_func(value)] = value

    def extend(self, values):
        pass

    def __iter__(self):
        pass
