# coding: utf8


class Gare(object):
    def __init__(self, name, distance=0):
        self._name = name
        self._distance = distance
        self._gares_available = []

    def add_gare_available(self, sub_tree):
        self._gares_available.append(sub_tree)

    def gareAccessibles(self):
        temp = []
        for gare in self._gares_available:
            temp.append(gare._name)

        return temp

    def __str__(self):
        msg = ""
        msg += "======================================\n"
        msg += "name: " + self._name
        msg += "\n"
        msg += "======================================\n"
        for gare in self._gares_available:
            msg += "gare: " + gare._name + " ,distance: " + gare._distance
            msg += "\n"
        msg += "======================================\n"
        return msg