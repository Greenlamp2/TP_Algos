# coding: utf8
from ReseauFerroviaire import ReseauFerroviaire

def match(parcour1, parcour2):
    for a in parcour1:
        for b in parcour2:
            if a == b:
                return a

    return None

def min_distance(chemins):
    if(chemins == []):
        return []
    else:
        return chemins[0]

def remove_after(parcour, ville):
    index = 0
    cpt = 0
    for elm in parcour:
        if elm == ville:
            index = cpt
        cpt += 1

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
                                b = remove_after(b, villeB)
                                distance = reseau.compute_distance(a)
                                distance += reseau2.compute_distance(b)
                                distance -= reseau2.compute_distance_int(b[0])
                                chemin = {
                                    "parcour": [a, list(reversed(b))],
                                    "distance": distance
                                }
                                chemins.append(chemin)
    return min_distance(chemins)


if __name__ == "__main__":
    reseaux = []

    reseau_bxl = ReseauFerroviaire()
    reseau_bxl.init_data("Bruxelles.txt")
    reseaux.append(reseau_bxl)

    reseau_rome = ReseauFerroviaire()
    reseau_rome.init_data("Rome.txt")
    reseaux.append(reseau_rome)


    print(trouverParcoursMin(reseaux, "Bruxelles", "Milan"))
    print(trouverParcoursMin(reseaux, "Bruxelles", "Bologne"))
    print(trouverParcoursMin(reseaux, "Bruxelles", "Florence"))
    print(trouverParcoursMin(reseaux, "Bruxelles", "Rome"))
    pass

