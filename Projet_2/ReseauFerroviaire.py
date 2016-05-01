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

    def get_or_create_node(self, name):
        node = self.get_node(name)
        if node == None:
            node = Gare(name)
            self._gares.append(node)

        return node

    def get_node(self, name):
        node = None
        for gare in self._gares:
            if gare._name == name:
                node = gare

        return node

    def garesAccessibles(self):
        self._temp = []
        self.rec_garesAccessibles(self.get_root()._name)
        return self._temp

    def rec_garesAccessibles(self, villeA):
        node = self.get_node(villeA)
        if(node != None):
            self._temp.append(node._name)
            if(node != None):
                temp = node.gareAccessibles()
                for item in temp:
                    self.rec_garesAccessibles(item)

    def existsParcours(self, villeA, destinations):
        possible = self.garesAccessibles(villeA)
        ok = True
        for destination in destinations:
            if destination not in possible:
                poss = self.garesAccessibles(destination)
                if villeA not in poss:
                    ok = False

        return ok

    def trouverParcours(self, destinations):
        parcours = []
        for destination in destinations:
            node_destination = self.get_node(destination)
            if(node_destination != None):
                parcour = self.get_parcours(self.get_root()._name, destination)
                if(len(parcour) > 0):
                    parcours.append(parcour)

        return parcours


    def get_parcours(self, villeA, villeB):
        self._temp = []
        node_villeB = self.get_node(villeB)
        node_villeA = self.get_node(villeA)
        if(node_villeB != None and node_villeA != None):
            self._temp = [node_villeB._name]
            self.rec_get_parcours(node_villeA, node_villeB)
            if(len(self._temp) == 1):
                self._temp = []
            else:
                self._temp = list(reversed(self._temp))
        else:
            self._temp = []
        return self._temp

    def rec_get_parcours(self, villeA, villeB):
        found = False
        for item in villeA._gares_available:
            if item._name == villeB._name:
                found = True
            if not found:
                found = self.rec_get_parcours(item, villeB)
        if found:
            self._temp.append(villeA._name)
        return found

    def trouverDistance(self, destinations):
        parcours = self.trouverParcours(destinations)
        distances = []
        for parcour in parcours:
            sum = 0
            for ville in parcour:
                node = self.get_node(ville)
                sum += int(node._distance)
            distances.append(sum)
        return distances

    def get_root(self):
        return self._gares[0]

    def compute_distance(self, parcour):
        distance = 0
        for ville in parcour:
            node = self.get_node(ville)
            if(node != None):
                distance += int(node._distance)

        return distance

    def compute_distance_int(self, ville):
        if ville == self.get_root()._name:
            return 0
        else:
            distance = self.trouverDistance([ville])
            return distance[-1]

    def __str__(self):
        msg = ""
        for gare in self._gares:
            msg += str(gare)
            msg += "\n"
        return msg
