# coding: utf8
from Node import Node

class ReseauFerroviaire(object):
    def __init__(self):
        self._tree = []

    def add_node(self, name, data, nb):
        if name == "Messina":
            pass
        node = Node(name)
        if nb != 0:
            for i in range(0, int(nb)):
                ville = data[i]
                distance = data[i+nb]
                node.add_gare(ville, distance)

        self._tree.append(node)

    def afficher(self):
        for node in self._tree:
            node.afficher()

    def init_data(self, name_file):
        with open(name_file, 'r') as f:
            read_data = f.read()

        for data in read_data.split("\n"):
            self.parse_node(data)
        try:
            pass
        except:
            print("Erreur de lecture du fichier.")

    def parse_node(self, data):
        item = data.split(";")
        name = item[0]

        nbItems = int(item[1])
        temp = []
        for i in range(1, nbItems+1):
            ville = item[1+i]
            temp.append(ville)

        for i in range(1, nbItems+1):
            distance = item[1+nbItems+i]
            temp.append(distance)

        self.add_node(name, temp, int(nbItems))

    def garesAccessibles(self):
        gares = []
        for node in self._tree:
            temp = node.gareAccessibles()
            for item in temp:
                if item not in gares:
                    gares.append(item)
        return gares

    def trouverParcours(self, destinations):
        pass

    def trouverDistance(self, destinations):
        pass