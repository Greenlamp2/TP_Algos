# coding: utf8
from Node import Node

class ReseauFerroviaire(object):
    def __init__(self):
        self._tree = []
        self._temp = []

    def add_node(self, name, data, nb):
        if name == "Messina":
            pass
        node = self.get_or_create_node(name)
        if nb != 0:
            for i in range(0, int(nb)):
                ville = data[i]
                sub_tree = self.get_or_create_node(ville)
                distance = data[i+nb]
                node.add_gare(ville, distance, sub_tree)

        self._tree.append(node)

    def get_or_create_node(self, name):
        node = self.get_node(name)
        if(node == None):
            node = self.create_node(name)
        return node

    def create_node(self, name):
        node = Node(name)
        self._tree.append(node)
        return node

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

    def garesAccessibles(self, villeA):
        self._temp = []
        self.rec_garesAccessibles(villeA)
        return self._temp

    def rec_garesAccessibles(self, villeA):
        self._temp.append(villeA)
        node = self.get_node(villeA)
        if(node == None):
            return
        temp = node.gareAccessibles()
        for item in temp:
            self.rec_garesAccessibles(item)


    def get_node(self, ville):
        for node in self._tree:
            if node._name == ville:
                return node

    def trouverParcours(self, villeA, destinations):
        node = self.get_node(villeA)
        return node.trouverParcours(destinations)

    def trouverDistance(self, destinations):
        pass