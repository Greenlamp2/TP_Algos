from Complexes import Complexes

if __name__ == "__main__":
    c1 = Complexes([(1,1), (2,2), (3,3)])
    print(c1)

    c1.addition(2, 2)
    print(c1)

    c1.multiply(2, 2)
    print(c1)