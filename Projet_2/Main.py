# coding: utf8
from ReseauFerroviaire import ReseauFerroviaire


def trouverParcoursMin(reseaux, villeA, villeB):
    chemins = []
    for reseau in reseaux:
        accessible = reseau.garesAccessibles()
        if villeA in accessible:
            parcour = reseau.get_parcours(villeA, villeB)
            if(parcour != []):
                distance = reseau.compute_distance(parcour)
                chemin = {
                    "parcour": parcour,
                    "distance": distance
                }
                chemins.append(chemin)
                print(parcour)
                print(distance)


if __name__ == "__main__":
    reseaux = []

    reseau_bxl = ReseauFerroviaire()
    reseau_bxl.init_data("Bruxelles.txt")
    print(reseau_bxl.garesAccessibles())
    print(reseau_bxl.trouverParcours(["Lille", "Paris", "Orleans"]))
    print(reseau_bxl.trouverDistance(["Lille", "Paris", "Orleans"]))
    reseaux.append(reseau_bxl)

    reseau_rome = ReseauFerroviaire()
    reseau_rome.init_data("Rome.txt")
    print(reseau_rome.garesAccessibles())
    print(reseau_rome.trouverParcours(["Messina", "Catania", "Trapani"]))
    print(reseau_rome.trouverDistance(["Messina", "Catania", "Trapani"]))
    reseaux.append(reseau_rome)


    trouverParcoursMin(reseaux, "Bruxelles", "Milan")

