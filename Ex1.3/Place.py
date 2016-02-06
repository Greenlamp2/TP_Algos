class Place(object):
    def __init__(self, data):
        self._data = data
        self._next = None
        self._prev = None

    def set_next(self, node):
        self._next = node

    def get_next(self):
        return self._next

    def set_prev(self, node):
        self._prev = node

    def get_prev(self):
        return self._prev

    def get_data(self):
        return self._data

    def get_prev(self):
        return self._prev