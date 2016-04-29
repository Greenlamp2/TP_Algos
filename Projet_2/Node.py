# coding: utf8
from Gare import Gare

class Node(object):
    def __init__(self, name):
        self._name = name
        self._gares = {}

    def add_gare(self, name, distance):
        gare = Gare(name, distance)
        self._gares[name] = gare

    def afficher(self):
        print("-----------------------")
        print("name: " + self._name)
        for key in self._gares.keys():
            self._gares[key].afficher()

    def gareAccessibles(self):
        temp = []
        for key in self._gares.keys():
            temp.append(self._gares[key]._name)

        return temp
