# coding: utf8
class Gare(object):
    def __init__(self, distance, root):
        self._root = root
        self._distance = distance

    def get_name(self):
        return self._root._name

    def afficher(self):
        print("gare: " + self.get_name() + " distance: " + self._distance)