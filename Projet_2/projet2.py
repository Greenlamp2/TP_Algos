# coding: utf8
from __future__ import print_function

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
        try:
            #On ouvre le fichier, et on lit tout dans la variable read_data
            with open(name_file, 'r') as f:
                read_data = f.read()

            #Pour chaques lignes, on passe dans la méthode parse_node
            for data in read_data.split("\n"):
                self.parse_node(data)
            return True
        except:
            print("Erreur de lecture du fichier "+ name_file +".")
            return False

    """
    parse_node
    Description:
        Permet de de parcourir les données extraite et de créer le reseau avec ceux-ci
    paramètre:
        - data: les données
    """
    def parse_node(self, data):
        #Les données sont séparés par des ;
        item = data.split(";")
        #Le premier elm sur la ligne étant le nom de la gare
        name = item[0]

        #Le second elm est le nombre de gares désservies
        nbItems = int(item[1])
        temp = []
        #On récupère ces gares
        for i in range(1, nbItems+1):
            ville = item[1+i]
            temp.append(ville)

        #On récupère ces distances
        for i in range(1, nbItems+1):
            distance = item[1+nbItems+i]
            temp.append(distance)

        #On ajoute cette gare au réseau
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
        #On crée ou récupere une node
        node = self.get_or_create_node(name)
        #Si on a au moins une ville désservie, on ajoute les distances etc
        if nb_ville != 0:
            #On parcours ces ville
            for i in range(0, int(nb_ville)):
                #Le nom de la ville
                ville = data[i]
                #On récupere la node ou on la crée
                sub_tree = self.get_or_create_node(ville)
                #On ajoute la distance
                distance = data[i+nb_ville]
                sub_tree._distance = distance
                #On ajoute la node aux gares déservies
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
        #On parcourt les gares désservies
        for gare in self._gares:
            #Si le nom est le même, on retourne l'element
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
        #On initialise la variable temporaire vide
        self._temp = []
        #On apelle la fonction récursive
        self.rec_garesAccessibles(self.get_root()._name)
        return self._temp

    """
    garesAccessibles
    Description:
        renvoie l'ensemble des villes atteignables depuis la racine, récursive
    paramètre:
    """
    def rec_garesAccessibles(self, villeA):
        #On récupere la node
        node = self.get_node(villeA)
        if(node != None):
            #On ajoute à la variable temporaire le nom de la ville
            self._temp.append(node._name)
            #On récupere les gares accessible
            temp = node.gareAccessibles()
            #On parcours ces gares accessibles
            for item in temp:
                #On rapelle cette fonction pour chaques gares accessible
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
        #Pour chaques destination
        for destination in destinations:
            #on récupere la node
            node_destination = self.get_node(destination)
            #Si elle existe
            if(node_destination != None):
                #On récupere le parcours entre la racine et la destination
                parcour = self.get_parcours(self.get_root()._name, destination)
                #Si le parcours existe
                if(len(parcour) > 0):
                    #On le rajoute dans la liste de parcours
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
        #On récupere les node des 2 villes
        node_villeB = self.get_node(villeB)
        node_villeA = self.get_node(villeA)
        #Si elles existent
        if(node_villeB != None and node_villeA != None):
            #On ajoute la ville d'arrivée dans la variable temporaire
            self._temp = [node_villeB._name]
            #On appelle la fonction récursive
            self.rec_get_parcours(node_villeA, node_villeB)
            #Si on qu'un seul elm, c'est que la fonction récursive n'a rien donnée
            if(len(self._temp) == 1):
                self._temp = []
            else:
                #Si on a des données, on les inverses
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
        #On parcourt toutes les villes dans les gares désservie
        for item in villeA._gares_available:
            #Si le nom est le même, c'est qu'on a trouver notre gare
            if item._name == villeB._name:
                #Found devient Vraie
                found = True
            #Si found n'est pas vraie, on refait un passage dans la fonction
            if not found:
                found = self.rec_get_parcours(item, villeB)
        #Si found est à vraie, ça veut dire qu'on a trouver lors d'un passage dans la fonction la gare ayant le nom
        #Qu'on recherchait
        if found:
            #On le rajoute à la liste
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
        #On recupere le parcours
        parcours = self.trouverParcours(destinations)
        distances = []
        #Pour chaques parcours
        for parcour in parcours:
            sum = 0
            #Pour chaques ville dans le parcour
            for ville in parcour:
                #On recupere la node
                node = self.get_node(ville)
                #On additionne les distances
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
        #Pour chaques ville dans le parcour
        for ville in parcour:
            #On récupere la node
            node = self.get_node(ville)
            #Si elle existe
            if(node != None):
                #On additionne la distance
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
        #Si la ville est la racine, on a pas bougé
        if ville == self.get_root()._name:
            return 0
        else:
            #On recupere la distance à partir de la ville qui n'est pas la racine
            distance = self.trouverDistance([ville])
            return distance[-1]

    def __str__(self):
        msg = ""
        for gare in self._gares:
            msg += str(gare)
            msg += "\n"
        return msg

    """
    match
    Description:
        Retourne la premiere ville commune entre 2 parcours
    paramètre:
        - parcour1: le premier parcour
        - parcour2: le second parcour
    """
def match(parcour1, parcour2):
    for a in parcour1:
        for b in parcour2:
            if a == b:
                return a

    return None

    """
    min_distance
    Description:
        Retourne le plus petit parcours parmis tout ceux trouvé
    paramètre:
        - chemins: les parcours trouvés.
    """
def min_distance(chemins):
    #On sauve le premier chemin et la premiere distance
    to_return = chemins[0]
    max = chemins[0]["distance"]
    #Pour chaques chemins
    for chemin in chemins:
        #Si la distance est plus petite, elle devient le chemin à retourner
        if chemin["distance"] < max:
            to_return = chemin
            max = chemin["distance"]

    return to_return

    """
    remove_after
    Description:
        Retire dans la liste les villes situé après la ville
    paramètre:
        - parcour: la liste
        - ville: la ville
    """
def remove_after(parcour, ville):
    #On récupere l'index de la ville dans la liste
    index = parcour.index(ville)
    if index != 0:
        #On récupere les X dernier element de la liste inversée
        temp = list(reversed(parcour))[:-index]
        #On retourne la liste inversé, étant la liste initiales - les elements retiré
        return list(reversed(temp))
    else:
        return parcour

    """
    remove_before
    Description:
        Retire dans la liste les villes situé avant la ville
    paramètre:
        - parcour: la liste
        - ville: la ville
    """
def remove_before(parcour, ville):
    index = parcour.index(ville)
    if index != 0:
        temp = list(reversed(parcour))[:-index]
        return list(reversed(temp))
    else:
        return parcour

    """
    trouverParcoursMin
    Description:
    qui renverra la plus petite chaine de gares entre deux villes, pas forcement
    situees dans le même arbre, si elle existe.
    paramètre:
        - reseaux: les réseaux disponible
        - villeA: la ville de départ
        - villeB: la ville d'arrivée
    """
def trouverParcoursMin(reseaux, villeA, villeB):
    #On initialise le tableau des chemins trouvée à vide
    chemins = []
    #Pour chaques réseau
    for reseau in reseaux:
        #On récupere les gares désservies
        accessible = reseau.garesAccessibles()
        #Si la villeA s'y trouve
        if villeA in accessible:
            #Si la ville B s'y trouve
            if villeB in accessible:
                #On récupere le parcours entre la villeA et la villeB
                parcour = reseau.get_parcours(villeA, villeB)
                #Si le parcours existe
                if(parcour != []):
                    #On récupere la distance entre la villeA et la villeB
                    distance = reseau.compute_distance(parcour)
                    #On retire la distance entre la racine et la villeA si celle-ci n'est pas la racine
                    distance -= reseau.compute_distance_int(villeA)
                    #On ajoute le parcour et la distance trouvée dnas la liste
                    chemin = {
                        "parcour": parcour,
                        "distance": distance
                    }
                    chemins.append(chemin)
            #Sinon, si la villeA s'y trouve mais pas la villeB
            else:
                #On va reparcourir les reseaux
                for reseau2 in reseaux:
                    #sauf la même que celle d'au dessus
                    if reseau2 != reseau:
                        #On récupere les gares désservies
                        accessible2 = reseau2.garesAccessibles()
                        #Si la villeB s'y trouve
                        if villeB in accessible2:
                            #On cherche une ville commune entre les 2 réseaux
                            middle = match(accessible, accessible2)
                            if(middle != None):
                                #On trouve le parcours dans le premier réseau jusqu'a cette ville commune
                                a = reseau.trouverParcours([middle])[-1]
                                #On trouve le parcours dans le second réseau jusqu'a cette ville commune
                                b = reseau2.trouverParcours([middle])[-1]
                                c = None
                                distance = 0
                                #Si la villeA n'est pas dans le premier réseau, c'est à dire qu'elle est dans une autre
                                #branche du réseau que celle liant la ville commune et la racine
                                if(villeA not in a):
                                    #On cherche donc le chemin vers cette ville depuis la racine
                                    c = reseau.trouverParcours([villeA])[-1]
                                #Si c'est le cas
                                if c!= None:
                                    #On récupere la distance entre la ville commune et la racine et on la rajoute à la
                                    #distance totale
                                    distance += reseau.compute_distance(c)
                                    #On inverse la liste
                                    c = list(reversed(c))
                                    #on retire le dernier elm qui est la racine
                                    del c[-1]
                                else:
                                    #Sinon, on retire les elm avant la villeA, sauf si c'est la racine
                                    a = remove_before(a, villeA)
                                #On retire les slms apres la villeB
                                b = remove_after(b, villeB)
                                #On calcule la distance entre la racine du réseau1 et le parcours vers la ville commune
                                distance += reseau.compute_distance(a)
                                #On calcule la distance entre la racine du réseau2 et le parcours vers la ville commune
                                distance += reseau2.compute_distance(b)
                                #On retire la distance entre la racine du réseau2 et la villeB
                                distance -= reseau2.compute_distance_int(b[0])
                                #On supprime la ville commune de la liste du réseau2
                                del b[-1]
                                #On inverse la liste
                                b = list(reversed(b))
                                #On additione le parcours du réseau 1 au réseau2
                                a.extend(b)
                                #Si on avait parcouru une autre branche avant
                                if c != None:
                                    #On ajoute à ce parcours, les 2 autres parcours
                                    c.extend(a)
                                    a = c
                                chemin = {
                                    "parcour": a,
                                    "distance": distance
                                }
                                chemins.append(chemin)
    return min_distance(chemins)

    """
    output
    Description:
        Met en forme la solution
    paramètre:
        - reponse: la réponse de la fonction trouvant le chemin
    """
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
    reseaux = [] #Création d'un tableau pour reprendre la liste des réseaux disponible

    reseau_bxl = ReseauFerroviaire() #Instanciation d'un réseau ferroviaire
    if reseau_bxl.init_data("Bruxelles.txt"): #Initialisation du réseau avec les données présentes dans Bruxelles.txt
        reseaux.append(reseau_bxl) #Ajout du réseau dans la liste des réseaux


    #IDEM
    reseau_rome = ReseauFerroviaire()
    if reseau_rome.init_data("Rome.txt"):
        reseaux.append(reseau_rome)


    #Appel de la fonction trouverParcrousMin avec affichage propre grâce à la fonction output)
    output(trouverParcoursMin(reseaux, "Bruxelles", "Milan"))
    output(trouverParcoursMin(reseaux, "Bruxelles", "Bologne"))
    output(trouverParcoursMin(reseaux, "Bruxelles", "Florence"))
    output(trouverParcoursMin(reseaux, "Bruxelles", "Rome"))
    output(trouverParcoursMin(reseaux, "Lille", "Milan"))
    output(trouverParcoursMin(reseaux, "Namur", "Rome"))
    output(trouverParcoursMin(reseaux, "Mons", "Rome"))
