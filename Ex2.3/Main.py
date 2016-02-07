def hanoi(n, a, c, b):
    """
    - On déplace les n-1 disque plus petits de la premiere à la seconde tour
    - On déplace le plus grand disque de la premiere à la troisieme tour
    - On déplace les n-1 disque de la deuxieme à la troisieme tour
    """

    if n != 0:
        hanoi(n-1, a, b, c)
        c.append(a[-1])
        a.remove(a[-1])
        hanoi(n-1, b, c, a)

if __name__ == "__main__":
    a = []
    b = []
    c = []
    n = 3

    for i in range(n):
        a.append(n-i)

    print("a:", end="")
    print(a)
    print("b:", end="")
    print(b)
    print("c:", end="")
    print(c)
    hanoi(n, a, c, b)
    print("algo")

    print("a:", end="")
    print(a)
    print("b:", end="")
    print(b)
    print("c:", end="")
    print(c)


