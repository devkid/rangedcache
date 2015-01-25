# RangedCache

RangedCache is a Python 3 implementation of a range based object cache. What does that mean?

Example: You use a GUI toolkit to display a List View to the user. The view is backed by a slow data source (database, network, etc.) and since your GUI toolkit does little to no caching for you, you can use RangedCache to speed up scrolling, etc.

Code:
```python
from rangedcache.rangedcache import RangedCache

class MyListModel(GUI.Model, RangedCache):
    # ...
    
    # called by RangedCache:
    def data(self, item):
        # slow operation:
        return self.myDataSource.data(item)
    def count(self):
        # might also be kinda slow
        return self.myDataSource.count()
    
    # ...
    
    # called by the List View:
    def giveMeData(self, row):
        # access cache instead of calling self.myDataSource.data()
        return self[row]
    def reset(self):
        # invalidate all data
        self.resetCache()
```

RangedCache is designed for accesses that read items that are near by ones that were read earlier. For example: intially, the List View from above displays the first few items of the data source. When the user scrolls down, RangedCache will automatically pre-fetch a defined number of lines from the data source and will have them available when the List View next wants to display them.
