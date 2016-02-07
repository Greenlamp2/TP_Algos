class Stack(object):
    def __init__(self, items=[]):
        self._items = items

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop(0)

    def top(self):
        return self.items[0]

    def size(self):
        return len(self._items)

    def is_empty(self):
        return self._items == []

    def copie(self):
        return Stack(self._items)

    def reverse(self):
        self._items = self._items[::-1]

    def __str__(self):
        line = ""
        for item in self._items:
            line = line + str(item)

        return line
