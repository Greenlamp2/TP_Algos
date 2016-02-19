def inverse(numbers, size):
    if(size > 0):
        inverse(numbers, size-1)
    print(numbers[len(numbers) - size-1], end=" ")


if __name__ == "__main__":
    numbers = [2, 8, 5, 9, 13, 11, 46, 51]
    print(numbers)

    inverse(numbers, len(numbers)-1)