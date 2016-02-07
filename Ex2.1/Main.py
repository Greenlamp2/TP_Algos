def get_max(liste, max):
    if(len(liste) == 0):
        return max
    elif(liste[0] > max):
        return get_max(liste[1:], liste[0])
    else:
        return get_max(liste[1:], max)



if __name__ == "__main__":
    liste = [245, 874, 214, 52, 147, 23, 65, 41]

    print("max: " + str(get_max(liste, -1)))