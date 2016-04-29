# coding: utf8
class Gare(object):
    def __init__(self, name, distance):
        self._name = name
        self._distance = distance

    def afficher(self):
        print("gare: " + self._name + " distance: " + self._distance)