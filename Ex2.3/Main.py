def hanoi(n, a, c, b):
    """
    - On déplace les n-1 disque plus petits de la premiere à la seconde tour
    - On déplace le plus grand disque de la premiere à la troisieme tour
    - On déplace les n-1 disque de la deuxieme à la troisieme tour
    """

    if n != 0:
        hanoi(n-1, a, b, c)
        c["data"].append(a["data"][-1])
        a["data"].remove(a["data"][-1])
        print("Déplacer un disque de " + a["id"] + " à " + c["id"])
        hanoi(n-1, b, c, a)

if __name__ == "__main__":
    a = {"id": "A", "data": []}
    b = {"id": "B", "data": []}
    c = {"id": "C", "data": []}
    n = 3

    for i in range(n):
        a["data"].append(n-i)

    hanoi(n, a, c, b)


