import unittest
import random
from rangedcache.rangedcache import RangedCache


class ObjectStore(RangedCache):

    def __init__(self, objects):
        super().__init__()
        self.objects = objects

    def data(self, range_):
        return self.objects[range_.start:range_.stop]

    def count(self):
        return len(self.objects)


class CacheBigEnoughTest(unittest.TestCase):
    """Simple equality test."""
    def setUp(self):
        self.objectStore = ObjectStore(random.sample(range(0, 10000), 50))

    def test_access(self):
        self.assertEqual(list(self.objectStore[0:self.objectStore.count()]), list(self.objectStore.objects))


class AccessesToRight(unittest.TestCase):
    """March the cache from the left to the right in steps smaller than the cache size."""
    def setUp(self):
        self.objectStore = ObjectStore(random.sample(range(0, 10000), 500))

    def test_access(self):
        count = self.objectStore.count()
        for i in range(0, count, 60):
            self.assertEqual(list(self.objectStore[i:max(i+10, count)]), list(self.objectStore.objects[i:max(i+10, count)]))


class AccessesToLeft(unittest.TestCase):
    """March the cache from the right to the left in steps smaller than the cache size."""
    def setUp(self):
        self.objectStore = ObjectStore(random.sample(range(0, 10000), 500))

    def test_access(self):
        for i in range(self.objectStore.count(), 0, -60):
            self.assertEqual(list(self.objectStore[min(0, i-10):i]), list(self.objectStore.objects[min(0, i-10):i]))


class GrowingStore(unittest.TestCase):
    """Simple equality test followed by march-right and march-left tests on a bigger store."""
    def setUp(self):
        self.objectStore = ObjectStore(random.sample(range(0, 10000), 50))

    def test_access(self):
        self.assertEqual(list(self.objectStore[0:50]), list(self.objectStore.objects))
        self.objectStore = ObjectStore(random.sample(range(0, 10000), 500))
        count = self.objectStore.count()
        for i in range(0, count, 60):
            self.assertEqual(list(self.objectStore[i:max(i+10, count)]), list(self.objectStore.objects[i:max(i+10, count)]))
        for i in range(self.objectStore.count(), 0, -60):
            self.assertEqual(list(self.objectStore[min(0, i-10):i]), list(self.objectStore.objects[min(0, i-10):i]))


class ShrinkingStore(unittest.TestCase):
    """Simple equality tests, one before and one after the shrinking."""
    def setUp(self):
        self.objectStore = ObjectStore(random.sample(range(0, 10000), 500))

    def test_access(self):
        self.assertEqual(list(self.objectStore[0:500]), list(self.objectStore.objects))
        self.objectStore = ObjectStore(random.sample(range(0, 10000), 50))
        self.assertEqual(list(self.objectStore[0:50]), list(self.objectStore.objects))

if __name__ == '__main__':
    unittest.main()
