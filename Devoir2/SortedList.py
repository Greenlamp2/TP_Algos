class SortedList(object):
    def __init__(self):
        self.head = Node("H", None)

    def insert(self, value):
        current = self.head.get_next()
        previous = self.head
        new_node = Node(value, None)
        while(current != None and current.get_value() < value):
                previous = current
                current = current.get_next()
        previous.set_next(new_node)
        new_node.set_next(current)


    def remove(self, value):
        current = self.head.get_next()
        previous = self.head
        while(current != None and current.get_value() < value):
            previous = current
            current = current.get_next()
        if(current != None and current.get_value() == value):
            previous.set_next(current.get_next())


    def search(self, value):
        found = False
        current = self.head.get_next()
        while(not found and current != None and current.get_value() < value):
            if(current.get_value() == value):
                found = True
            else:
                current = current.get_next()
        return current

    def __iter__(self):
        current = self.head.get_next()
        while current is not None:
            yield current.get_value()
            current = current.get_next()


class Node(object):
    def __init__(self, value, next):
        self._value = value
        self._next = next

    def get_next(self):
        return self._next

    def set_next(self, next):
        self._next = next

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value