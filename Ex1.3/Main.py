from Liste import *

if __name__ == "__main__":
    listComplexes = Liste()
    listComplexes.add_item((1, 2))
    listComplexes.add_item((3, 4))
    print(listComplexes)

    print("last element:" )
    print(listComplexes.fin().get_data())