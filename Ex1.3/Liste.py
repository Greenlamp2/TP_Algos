from Place import *

class Liste(object):
    def __init__(self):
        self._head = Place(-1)
        self._head.set_next(self._head)
        self._length = 0

    def one_more(self):
        self._length = self._length + 1

    def one_less(self):
        self._length = self._length - 1

    def add_item(self, item):
        node = Place(item)
        node.set_next(self._head.get_next())
        node.set_prev(self._head.get_prev())
        self._head.set_next(node)
        if(self._head.get_prev() == None):
            self._head.set_prev(node)
        self.one_more()

    def add_after_item(self, what, item):
        node = Place(item)
        node.set_next(what.get_next())
        what.set_next(node)
        self.one_more()

    def size(self):
        return self._length

    def search(self, item):
        current = self._head
        found = False
        while current != self._head and not found:
            if(current.get_data() == item):
                found = True
            else:
                current = current.get_next()
        return False

    def remove(self, what):
        previous = self._head
        current = self._head.get_next()
        found = False
        while current != self._head and not found:
            if current is what:
                found = True
            else:
                previous = current
                current = current.get_next()
        if found:
            previous.set_next(what.get_next())

    def __str__(self):
        line = ""
        current = self._head.get_next()
        data = current.get_data()
        while data != -1:
            line = line + "(" + str(data[0]) + " + " + str(data[1]) + "i)"
            current = current.get_next()
            data = current.get_data()
        return line

    def fin(self):
        return self._head.get_prev()