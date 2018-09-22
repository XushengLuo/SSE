class Item(object):
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar
    def __repr__(self):
        return "Item(%s, %s)" % (self.foo, self.bar)
    def __eq__(self, other):
        if isinstance(other, Item):
            return ((self.foo == other.foo) and (self.bar == other.bar))
        else:
            return False
    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash((self.foo, self.bar))

a = set()
a.add(Item(1,2))
b = Item(1,2)
print(b in a)