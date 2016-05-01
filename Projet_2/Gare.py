# coding: utf8


class Gare(object):
    """
    Constructeur
    Paramètre:
        - name: Le nom de la gare
        - distance: La distance entre cette gare et son père
        - gares_available: Gares désservie depuis celle-ci
    attributs:
        - name: Le nom de la gare
        - distance: La distance entre cette gare et son père
        - gares_available: Gares désservie depuis celle-ci
    """
    def __init__(self, name, distance=0):
        self._name = name
        self._distance = distance
        self._gares_available = []

    """
    add_gare_available
    Description:
        Rajoute une nouvelle gare désservie
    paramètre:
        - sub_tree: la nouvelle gare
    """
    def add_gare_available(self, sub_tree):
        self._gares_available.append(sub_tree)

    """
    gareAccessibles
    Description:
        Retourne la liste des gares désservie
    paramètre:
    """
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