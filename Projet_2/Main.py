# coding: utf8
from ReseauFerroviaire import ReseauFerroviaire


def trouverParcoursMin(reseau, villeA, villeB):
    pass


if __name__ == "__main__":
    reseau = ReseauFerroviaire()
    reseau.init_data("data.txt")
    print(reseau.garesAccessibles("Messina"))

    print(reseau.trouverParcours("Messina", ["Catania", "Palermo", "Rome"]))