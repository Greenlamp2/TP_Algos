def Place(object):
    def __init__(self, data):
        self._data = data
        self._next = None

    def set_next(self, node):
        self._next = node

    def get_next(self):
        return self._next

    def get_data(self):
        return self._data