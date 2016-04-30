# coding: utf8
from Gare import Gare


class ReseauFerroviaire(object):
    def __init__(self):
        self._gares = []
        self._temp = None

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

    def add_node(self, name, data, nb_ville):
        node = self.get_or_create_node(name)
        if nb_ville != 0:
            for i in range(0, int(nb_ville)):
                ville = data[i]
                sub_tree = self.get_or_create_node(ville)
                distance = data[i+nb_ville]
                sub_tree._distance = distance
                node.add_gare_available(sub_tree)

        self._gares.append(node)

    def get_or_create_node(self, name):
        node = self.get_node(name)
        if node == None:
            node = Gare(name)

        return node

    def get_node(self, name):
        node = None
        for gare in self._gares:
            if gare._name == name:
                node =  gare

        return node

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

    def trouverParcours(self, villeA, destinations):
        possible = self.garesAccessibles(villeA)
        ok = True
        for destination in destinations:
            if destination not in possible:
                poss = self.garesAccessibles(destination)
                if villeA not in poss:
                    ok = False

        return ok

    def get_parcours(self, villeA, villeB):
        return []

    def trouverDistance(self, villeA, destinations):
        pass

    def __str__(self):
        msg = ""
        for gare in self._gares:
            msg += str(gare)
            msg += "\n"
        return msg
