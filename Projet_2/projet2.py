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



class ReseauFerroviaire(object):
    """
    Constructeur
    Paramètre:
    attributs:
        - gares: les gares qui composent ce réseau
        - temp: Variable temporaire pour stocker le chemin lors de passage récursif dans certaines méthodes
    """
    def __init__(self):
        self._gares = []
        self._temp = None

    """
    init_data
    Description:
        Permet de lire le fichier data et d'y extraire les informations des gares
    paramètre:
        - name_file: le nom du fichier
    """
    def init_data(self, name_file):
        with open(name_file, 'r') as f:
            read_data = f.read()

        for data in read_data.split("\n"):
            self.parse_node(data)
        try:
            pass
        except:
            print("Erreur de lecture du fichier.")

    """
    parse_node
    Description:
        Permet de de parcourir les données extraite et de créer le reseau avec ceux-ci
    paramètre:
        - data: les données
    """
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

    """
    add_node
    Description:
        Permet d'ajouter une node/Gare dans le réseau
    paramètre:
        - name: le nom de la ville
        - data: les informations reprenant les gares désservies et leur distances
        - nb_ville: le nombre de gares désservies.
    """
    def add_node(self, name, data, nb_ville):
        node = self.get_or_create_node(name)
        if nb_ville != 0:
            for i in range(0, int(nb_ville)):
                ville = data[i]
                sub_tree = self.get_or_create_node(ville)
                distance = data[i+nb_ville]
                sub_tree._distance = distance
                node.add_gare_available(sub_tree)

    """
    get_or_create_node
    Description:
        Permet de créer une nouvelle node ou de récupérer la node si elle existe déja
    paramètre:
        - name: le nom de la ville
    """
    def get_or_create_node(self, name):
        node = self.get_node(name)
        if node == None:
            node = Gare(name)
            self._gares.append(node)

        return node

    """
    get_or_create_node
    Description:
        Permet de récupérer une node par son nom
    paramètre:
        - name: le nom de la ville
    """
    def get_node(self, name):
        node = None
        for gare in self._gares:
            if gare._name == name:
                node = gare

        return node

    """
    garesAccessibles
    Description:
        renvoie l'ensemble des villes atteignables depuis la racine, appelant la méthode récursive
    paramètre:
    """
    def garesAccessibles(self):
        self._temp = []
        self.rec_garesAccessibles(self.get_root()._name)
        return self._temp

    """
    garesAccessibles
    Description:
        renvoie l'ensemble des villes atteignables depuis la racine, récursive
    paramètre:
    """
    def rec_garesAccessibles(self, villeA):
        node = self.get_node(villeA)
        if(node != None):
            self._temp.append(node._name)
            if(node != None):
                temp = node.gareAccessibles()
                for item in temp:
                    self.rec_garesAccessibles(item)

    """
    trouverParcours
    Description:
        qui prend en parametre une liste de destinations possibles, presentes
        dans un arbre, et qui renvoie tous les chemins dans l'arbre allant de la racine de depart aux villes
        presentes dans la liste
    paramètre:
        - destinations: les destinations possibles
    """
    def trouverParcours(self, destinations):
        parcours = []
        for destination in destinations:
            node_destination = self.get_node(destination)
            if(node_destination != None):
                parcour = self.get_parcours(self.get_root()._name, destination)
                if(len(parcour) > 0):
                    parcours.append(parcour)

        return parcours

    """
    get_parcours
    Description:
        récupere le parcours d'une villeA à une villeB, appelant la méthode récursive
    paramètre:
        - VilleA: la ville de départ
        - VilleB: la ville d'arrivée
    """
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

    """
    rec_get_parcours
    Description:
        récupere le parcours d'une villeA à une villeB, récursive
    paramètre:
        - VilleA: la ville de départ
        - VilleB: la ville d'arrivée
    """
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

    """
    trouverDistance
    Description:
        qui prend en parametre une liste de destinations possibles, presentes
        dans un arbre, et qui renvoie la distance en kilometres entre la ville de depart et les villes presentes dans
        la liste
    paramètre:
        - destinations: les destinations possibles
    """
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

    """
    get_root
    Description:
        retourne la racine
    paramètre:
    """
    def get_root(self):
        return self._gares[0]

    """
    compute_distance
    Description:
        Calcule la distance totale parcourue depuis la racine
    paramètre:
        - parcour: le parcours
    """
    def compute_distance(self, parcour):
        distance = 0
        for ville in parcour:
            node = self.get_node(ville)
            if(node != None):
                distance += int(node._distance)

        return distance

    """
    compute_distance_int
    Description:
        Calcule la distance entre la racine et une ville choisie
    paramètre:
        - ville: la ville choisie
    """
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

def match(parcour1, parcour2):
    for a in parcour1:
        for b in parcour2:
            if a == b:
                return a

    return None

def min_distance(chemins):
    to_return = chemins[0]
    max = chemins[0]["distance"]
    for chemin in chemins:
        if chemin["distance"] < max:
            to_return = chemin
            max = chemin["distance"]

    return to_return

def remove_after(parcour, ville):
    # index = 0
    # cpt = 0
    # for elm in parcour:
    #     if elm == ville:
    #         index = cpt
    #     cpt += 1

    index = parcour.index(ville)
    if index != 0:
        temp = list(reversed(parcour))[:-index]
        return list(reversed(temp))
    else:
        return parcour

def remove_before(parcour, ville):
    # index = 0
    # cpt = 0
    # for elm in parcour:
    #     if elm == ville:
    #         index = cpt
    #     cpt += 1

    index = parcour.index(ville)
    if index != 0:
        temp = list(reversed(parcour))[:-index]
        return list(reversed(temp))
    else:
        return parcour

def trouverParcoursMin(reseaux, villeA, villeB):
    chemins = []
    for reseau in reseaux:
        accessible = reseau.garesAccessibles()
        if villeA in accessible:
            if villeB in accessible:
                parcour = reseau.get_parcours(villeA, villeB)
                if(parcour != []):
                    distance = reseau.compute_distance(parcour)
                    distance -= reseau.compute_distance_int(villeA)
                    chemin = {
                        "parcour": parcour,
                        "distance": distance
                    }
                    chemins.append(chemin)
            else:
                for reseau2 in reseaux:
                    if reseau2 != reseau:
                        accessible2 = reseau2.garesAccessibles()
                        if villeB in accessible2:
                            middle = match(accessible, accessible2)
                            if(middle != None):
                                a = reseau.trouverParcours([middle])[-1]
                                b = reseau2.trouverParcours([middle])[-1]
                                c = None
                                distance = 0
                                if(villeA not in a):
                                    c = reseau.trouverParcours([villeA])[-1]
                                if c!= None:
                                    distance += reseau.compute_distance(c)
                                    c = list(reversed(c))
                                    del c[-1]
                                else:
                                    a = remove_before(a, villeA)
                                b = remove_after(b, villeB)
                                distance += reseau.compute_distance(a)
                                distance += reseau2.compute_distance(b)
                                distance -= reseau2.compute_distance_int(b[0])
                                del b[-1]
                                b = list(reversed(b))
                                a.extend(b)
                                if c != None:
                                    c.extend(a)
                                    a = c
                                chemin = {
                                    "parcour": a,
                                    "distance": distance
                                }
                                chemins.append(chemin)
    return min_distance(chemins)


def output(reponse):
    if reponse == None:
        print("Aucuns parcours possible")
    else:
        villeA = reponse["parcour"][0]
        villeB = reponse["parcour"][-1]
        print("Meilleur Parcours possible entre " + villeA + " et " + villeB + " :")
        for elm in enumerate(reponse["parcour"]):
            if(elm[0] != len(reponse["parcour"])-1):
                print(elm[1], end=", ")
            else:
                print(elm[1])
        print("Distance: " + str(reponse["distance"]))


if __name__ == "__main__":
    reseaux = []

    reseau_bxl = ReseauFerroviaire()
    reseau_bxl.init_data("Bruxelles.txt")
    reseaux.append(reseau_bxl)

    reseau_rome = ReseauFerroviaire()
    reseau_rome.init_data("Rome.txt")
    reseaux.append(reseau_rome)


    output(trouverParcoursMin(reseaux, "Bruxelles", "Milan"))
    output(trouverParcoursMin(reseaux, "Bruxelles", "Bologne"))
    output(trouverParcoursMin(reseaux, "Bruxelles", "Florence"))
    output(trouverParcoursMin(reseaux, "Bruxelles", "Rome"))
    output(trouverParcoursMin(reseaux, "Lille", "Milan"))
    output(trouverParcoursMin(reseaux, "Namur", "Rome"))
    output(trouverParcoursMin(reseaux, "Mons", "Rome"))
    pass

