def reverse(new_liste, liste, size):
    if(size == 0):
        return new_liste
    else:
        number = liste[size-1:][0]
        new_liste.append(number)
        return reverse(new_liste,liste, size-1)


if __name__ == "__main__":
    liste = [245, 874, 214, 52, 147, 23, 65, 41]
    print("liste")
    print(liste)
    print("reversing")
    liste2 = reverse([], liste, len(liste))
    print("liste")
    print(liste)
    print("liste2")
    print(liste2)