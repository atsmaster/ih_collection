
class ItemPool:
    item_pool = dict()

    def add(self, item):
        self.item_pool[item.id] = item

    def get(self, key):
        return self.item_pool.get(key)