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
    def __init__(self, nom, distance=0):
        self.nom = nom
        self.distance = distance
        self.gares = []

    """
    nouvelleGare
    Description:
        Rajoute une nouvelle gare désservie
    paramètre:
        - sub_tree: la nouvelle gare
    """
    def nouvelleGare(self, gare):
        self.gares.append(gare)

    """
    gareAccessibles
    Description:
        Retourne la liste des gares désservie
    paramètre:
    """
    def gareAccessibles(self):
        a = []
        for gare in self.gares:
            a.append(gare.nom)

        return a

class ReseauFerroviaire(object):
    """
    Constructeur
    Paramètre:
    attributs:
        - gares: les gares qui composent ce réseau
        - temp: Variable temporaire pour stocker le chemin lors de passage récursif dans certaines méthodes
    """
    def __init__(self):
        self.gares = []
        self.chemin = None

    def ajout(self, nom, villes, distances):
        #On crée ou récupere une node
        node = self.getNode(nom, True)
        for ville, distance in zip(villes, distances):
            gare = self.getNode(ville, True)
            gare.distance = distance
            #On ajoute la node aux gares déservies
            node.nouvelleGare(gare)
    """
    getNode
    Description:
        Permet de créer une nouvelle node ou de récupérer la node si elle existe déja
    paramètre:
        - name: le nom de la ville
    """
    def getNode(self, name, ajout=False):
        node = None
        #On parcourt les gares désservies
        for gare in self.gares:
            #Si le nom est le même, on retourne l'element
            if gare.nom == name:
                node = gare
        if node == None and ajout:
            node = Gare(name)
            self.gares.append(node)

        return node

    """
    garesAccessibles
    Description:
        renvoie l'ensemble des villes atteignables depuis la racine, appelant la méthode récursive
    paramètre:
    """
    def garesAccessibles(self):
        #On initialise la variable temporaire vide
        self.chemin = []
        #On apelle la fonction récursive
        self.gareAccess(self.get_root().nom)
        return self.chemin

    """
    garesAccessibles
    Description:
        renvoie l'ensemble des villes atteignables depuis la racine, récursive
    paramètre:
    """
    def gareAccess(self, villeA):
        #On récupere la node
        node = self.getNode(villeA)
        if(node != None):
            #On ajoute à la variable temporaire le nom de la ville
            self.chemin.append(node.nom)
            #On récupere les gares accessible
            a = node.gareAccessibles()
            #On parcours ces gares accessibles
            for item in a:
                #On rapelle cette fonction pour chaques gares accessible
                self.gareAccess(item)

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
            dest = self.getNode(destination)
            #Si elle existe
            if(dest != None):
                #On récupere le parcours entre la racine et la destination
                parcour = self.getParcours(self.get_root().nom, destination)
                #Si le parcours existe
                if(len(parcour) > 0):
                    #On le rajoute dans la liste de parcours
                    parcours.append(parcour)

        return parcours

    """
    getParcours
    Description:
        récupere le parcours d'une villeA à une villeB, appelant la méthode récursive
    paramètre:
        - VilleA: la ville de départ
        - VilleB: la ville d'arrivée
    """
    def getParcours(self, villeA, villeB):
        self.chemin = []
        #On récupere les node des 2 villes
        nodeB = self.getNode(villeB)
        nodeA = self.getNode(villeA)
        #Si elles existent
        if(nodeB != None and nodeA != None):
            #On ajoute la ville d'arrivée dans la variable temporaire
            self.chemin = [nodeB.nom]
            #On appelle la fonction récursive
            self.getParc(nodeA, nodeB)
            #Si on qu'un seul elm, c'est que la fonction récursive n'a rien donnée
            if(len(self.chemin) == 1):
                self.chemin = []
            else:
                #Si on a des données, on les inverses
                self.chemin = list(reversed(self.chemin))
        else:
            self.chemin = []
        return self.chemin

    """
    getParc
    Description:
        récupere le parcours d'une villeA à une villeB, récursive
    paramètre:
        - VilleA: la ville de départ
        - VilleB: la ville d'arrivée
    """
    def getParc(self, villeA, villeB):
        found = False
        #On parcourt toutes les villes dans les gares désservie
        for item in villeA.gares:
            #Si le nom est le même, c'est qu'on a trouver notre gare
            if item.nom == villeB.nom:
                #Found devient Vraie
                found = True
            #Si found n'est pas vraie, on refait un passage dans la fonction
            if not found:
                found = self.getParc(item, villeB)
        #Si found est à vraie, ça veut dire qu'on a trouver lors d'un passage dans la fonction la gare ayant le nom
        #Qu'on recherchait
        if found:
            #On le rajoute à la liste
            self.chemin.append(villeA.nom)
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
            cpt = 0
            #Pour chaques ville dans le parcour
            for ville in parcour:
                #On recupere la node
                node = self.getNode(ville)
                #On additionne les distances
                cpt += int(node.distance)
            distances.append(cpt)
        return distances

    """
    get_root
    Description:
        retourne la racine
    paramètre:
    """
    def get_root(self):
        return self.gares[0]

    """
    calculer
    Description:
        Calcule la distance totale parcourue depuis la racine
    paramètre:
        - parcour: le parcours
    """
    def calculer(self, chemin):
        distance = 0
        #Pour chaques ville dans le parcour
        for ville in chemin:
            #On récupere la node
            node = self.getNode(ville)
            #Si elle existe
            if(node != None):
                #On additionne la distance
                distance += int(node.distance)

        return distance

    """
    calculerDepuis
    Description:
        Calcule la distance entre la racine et une ville choisie
    paramètre:
        - ville: la ville choisie
    """
    def calculerDepuis(self, ville):
        #Si la ville est la racine, on a pas bougé
        if ville == self.get_root().nom:
            return 0
        else:
            #On recupere la distance à partir de la ville qui n'est pas la racine
            distance = self.trouverDistance([ville])
            return distance[-1]

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
    #Pour chaques réseau
    for reseau in reseaux:
        #On récupere les gares désservies
        accessible = reseau.garesAccessibles()
        #Si la villeA s'y trouve
        if villeA in accessible:
            #Si la ville B s'y trouve
            if villeB in accessible:
                #On récupere le parcours entre la villeA et la villeB
                parcour = reseau.getParcours(villeA, villeB)
                #Si le parcours existe
                if(parcour != []):
                    #On récupere la distance entre la villeA et la villeB
                    distance = reseau.calculer(parcour)
                    #On retire la distance entre la racine et la villeA si celle-ci n'est pas la racine
                    distance -= reseau.calculerDepuis(villeA)
                    return [parcour, distance]
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

                            correspondance = None
                            for elm in accessible:
                                for elm2 in accessible2:
                                    if elm == elm2:
                                        correspondance = elm
                            if(correspondance != None):
                                #On trouve le parcours dans le premier réseau jusqu'a cette ville commune
                                parcoursA = reseau.trouverParcours([correspondance])[-1]
                                #On trouve le parcours dans le second réseau jusqu'a cette ville commune
                                parcoursB = reseau2.trouverParcours([correspondance])[-1]
                                parcoursC = None
                                distance = 0
                                #Si la villeA n'est pas dans le premier réseau, c'est à dire qu'elle est dans une autre
                                #branche du réseau que celle liant la ville commune et la racine
                                if(villeA not in parcoursA):
                                    #On cherche donc le chemin vers cette ville depuis la racine
                                    parcoursC = reseau.trouverParcours([villeA])[-1]
                                #Si c'est le cas
                                if parcoursC!= None:
                                    #On récupere la distance entre la ville commune et la racine et on la rajoute à la
                                    #distance totale
                                    distance += reseau.calculer(parcoursC)
                                    #On inverse la liste
                                    parcoursC = list(reversed(parcoursC))
                                    #on retire le dernier elm qui est la racine
                                    del parcoursC[-1]
                                else:
                                    #Sinon, on retire les elm avant la villeA, sauf si c'est la racine
                                    index = parcoursA.index(villeA)
                                    if index != 0:
                                        #On récupere les X dernier element de la liste inversée
                                        temp = list(reversed(parcoursA))[:-index]
                                        #On retourne la liste inversé, étant la liste initiales - les elements retiré
                                        parcoursA = list(reversed(temp))
                                #On retire les slms apres la villeB
                                index = parcoursB.index(villeB)
                                if index != 0:
                                    #On récupere les X dernier element de la liste inversée
                                    temp = list(reversed(parcoursB))[:-index]
                                    #On retourne la liste inversé, étant la liste initiales - les elements retiré
                                    parcoursB = list(reversed(temp))
                                #On calcule la distance entre la racine du réseau1 et le parcours vers la ville commune
                                distance += reseau.calculer(parcoursA)
                                #On calcule la distance entre la racine du réseau2 et le parcours vers la ville commune
                                distance += reseau2.calculer(parcoursB)
                                #On retire la distance entre la racine du réseau2 et la villeB
                                distance -= reseau2.calculerDepuis(parcoursB[0])
                                #On supprime la ville commune de la liste du réseau2
                                del parcoursB[-1]
                                #On inverse la liste
                                parcoursB = list(reversed(parcoursB))
                                #On additione le parcours du réseau 1 au réseau2
                                parcoursA.extend(parcoursB)
                                #Si on avait parcouru une autre branche avant
                                if parcoursC != None:
                                    #On ajoute à ce parcours, les 2 autres parcours
                                    parcoursC.extend(parcoursA)
                                    parcoursA = parcoursC
                                return [parcoursA, distance]


if __name__ == "__main__":
    reseaux = [] #Création d'un tableau pour reprendre la liste des réseaux disponible

    reseau_bxl = ReseauFerroviaire() #Instanciation d'un réseau ferroviaire
    #Initialisation du réseau avec les données présentes dans Bruxelles.txt
    reseau_bxl.ajout("Bruxelles", ["Liege", "Lille"], [96, 120])
    reseau_bxl.ajout("Liege", ["Spa", "Namur"], [39, 65])
    reseau_bxl.ajout("Spa", [], [])
    reseau_bxl.ajout("Namur", ["Charleroi", "Arlon"], [50, 128])
    reseau_bxl.ajout("Charleroi", ["Mons"], [50])
    reseau_bxl.ajout("Mons", [], [])
    reseau_bxl.ajout("Arlon", [], [])
    reseau_bxl.ajout("Lille", ["Londre", "Paris"], [292, 223])
    reseau_bxl.ajout("Paris", ["orleans", "Lyon", "Borges"], [129, 465, 245])
    reseau_bxl.ajout("Lyon", ["Geneve", "Milan"], [150, 442])
    reseau_bxl.ajout("Geneve", [], [])
    reseau_bxl.ajout("Milan", [], [])
    reseaux.append(reseau_bxl) #Ajout du réseau dans la liste des réseaux


    #IDEM
    reseau_rome = ReseauFerroviaire()
    reseau_rome.ajout("Rome", ["Florence", "Naples"], [278, 225])
    reseau_rome.ajout("Florence", ["Pisa", "Bologna"], [82, 104])
    reseau_rome.ajout("Pisa", [], [])
    reseau_rome.ajout("Bologna", ["Venice", "Milan"], [145, 222])
    reseau_rome.ajout("Venice", ["Vicenza"], [75])
    reseau_rome.ajout("Vicenza", [], [])
    reseau_rome.ajout("Milan", [], [])
    reseaux.append(reseau_rome)


    #Appel de la fonction trouverParcrousMin avec affichage propre grâce à la fonction output)
    print(trouverParcoursMin(reseaux, "Bruxelles", "Rome"))
    print(trouverParcoursMin(reseaux, "Namur", "Rome"))
