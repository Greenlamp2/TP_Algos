def good_power(number, power):
    num = number / power
    if num == power or num == 1:
        return True
    elif num > power:
        return good_power(num, power)
    else:
        return False


def get_max(suite):
    max = suite[0]
    for i in range(len(suite)):
        if(suite[i] > max):
            max = suite[i]

    return max


if __name__ == "__main__":
    character = None
    suite = []
    sub = []
    while(character != "-1"):
        print("enter a power of 2")
        character = input()
        try:
            number = int(character)
            if(good_power(number, 2) or number == -1):
                suite.append(number)
            else:
                print("this is not a power of 2")
        except:
            print("this is not a number")

    #suite = [128, 8, 4, 16, 64, 512, 2, 32, -1]
    suite.remove(suite[-1])

    max = suite[0]
    while(len(suite) > 0 and max != suite[-1]):
        max = get_max(suite)
        sub.append(max)
        num = suite.index(max)+1
        suite = suite[num:]

    print(sub)

