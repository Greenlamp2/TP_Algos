def pair_impair(numbers, size):
    if(size >= 0):
        n = len(numbers) - size - 1
        if(numbers[n] % 2 == 0):
            print(numbers[n], end=" ")
            pair_impair(numbers, size - 1)
        else:
            pair_impair(numbers, size - 1)
            print(numbers[n], end=" ")

if __name__ == "__main__":
    numbers = [2, 5, 8, 9, 11, 13, 46, 51]
    n = len(numbers)
    pair_impair(numbers, n-1)