def inverse(size):
    number = None
    if(size > 0):
        print("enter a number:")
        number = input()
        inverse(size-1)
        print(number)


if __name__ == "__main__":

    print("How many numbers ?")
    number = input()
    try:
        inverse(int(number))
    except:
        print("bad number")