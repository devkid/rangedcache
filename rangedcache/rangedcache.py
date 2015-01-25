class RangedCache:

    def __init__(self, radius=100):
        """Initializes the cache without populating it, i.e. without request data from the underlying object store yet.

        radius -- The radius around a requested row that will be pre-fetched if the row is not yet cached.
        """
        self.__radius = radius
        self.__range = range(0)
        self.__cache = []

    def __getitem__(self, row):
        """Subscription implementation with slice support.
        """
        if isinstance(row, int):
            if row not in self.__range:
                self.__recenter(row)
            return self.__cache[row - self.__range.start]
        elif isinstance(row, slice):
            return map(lambda i: self.__getitem__(i), range(row.start, row.stop))

    def __recenter(self, row):
        """Re-centers the cache around the given row.

        This will make sure that `row` is the new center of the cache. If the new caching range overlaps with the old,
        the objects from the overlapping range are used and not requested again.
        """

        # step 1: calculate new range
        # ---------------------------

        count = self.count()
        oldRange = self.__range

        # case 1: all objects fit into the cache
        size = 2 * self.__radius
        if count < size:
            newRange = range(0, size)

        # case 2: requested row is too near to 0; range is extended to the right
        elif row < self.__radius:
            extra = self.__radius - row + 0
            newRange = range(0, row + self.__radius + extra)

        # case 3: requested row is too near to count; range is extended to the left
        elif row > count - self.__radius:
            extra = self.__radius + row - count
            newRange = range(row - self.__radius - extra, count)

        # case 4: neither of the above
        else:
            newRange = range(row - self.__radius, row + self.__radius)

        # step 2: detect range overlapping to reuse data
        # ----------------------------------------------

        # overlap[0] indicates the position of the old range in relation to the new range (-1 = left, +1 = right)

        if len(oldRange) > 0:

            # case 1: right side of old range overlaps left side of new range
            if oldRange.start < newRange.start < oldRange.stop:
                overlap = (-1, range(newRange.start, oldRange.stop))

            # case 2: left side of old range overlaps right side of new range
            elif oldRange.start < newRange.stop < oldRange.stop:
                overlap = (+1, range(oldRange.start, newRange.stop))

            # case 3: neither of the above
            else:
                overlap = None

        else:
            overlap = None

        # step 3: fill new cache
        # ----------------------------

        if overlap is None:
            self.__cache = self.data(newRange)
        else:
            reuse = self.__cache[overlap[1].start-oldRange.start:overlap[1].stop-oldRange.start]

            if overlap[0] < 0:
                renew = range(overlap[1].stop, newRange.stop)
                self.__cache = reuse + self.data(renew)
            else:
                renew = range(newRange.start, overlap[1].start)
                self.__cache = self.data(renew) + reuse

        # finally: update range
        self.__range = newRange

    def resetCache(self):
        self.__range = range(0)
        self.__cache = []
