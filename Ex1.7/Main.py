from Stack import Stack

if __name__ == "__main__":
    stack = Stack([1, 2, 3, 4, 5])
    print("pile 1:")
    print(stack)

    stack2 = stack.copie()
    stack2.reverse()
    print("reversing")
    print("pile 1:")
    print(stack)
    print("pile 2:")
    print(stack2)