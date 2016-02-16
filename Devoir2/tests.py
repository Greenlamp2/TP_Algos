from SortedList import SortedList
from random import randint, choice

TEST_SIZE = 50

def random_list(app_size):
    L = SortedList()
    for v in list(set([randint(0,99) for _ in range(app_size)])):
        L.insert(v)
    return L

def equiv(L,l):
    return list(L) == l

def test_insert():
    
    L = SortedList()
    test_list = [randint(0,99) for _ in range(TEST_SIZE)]

    for v in test_list:
        L.insert(v)

    test_list.sort()
    return equiv(L, test_list)

    
def test_remove():
    
    L = random_list(50)
    test_list = list(L)

    to_remove = choice(test_list)

    L.remove(to_remove)
    test_list.remove(to_remove)

    return equiv(L, test_list)


def test_search():
    
    L = random_list(50)
    test_list = list(L)

    to_search = choice(test_list)

    found = L.search(to_search)
    
    return found is not None and found.get_value() == to_search

def run_all_tests():
    print("Test Insert...",end = "") 
    insert_OK = test_insert()
    print("OK" if insert_OK else "NOT OK") 
    if not insert_OK: print("\"Yeah, if you could fix insert before, that would be great\" - Bill Lumbergh")

    print("Test Remove...",end = "") 
    remove_OK = all([test_remove() for _ in range(TEST_SIZE)])
    print("OK" if remove_OK else "NOT OK")

    print("Test Search...",end = "") 
    search_OK = all([test_search() for _ in range(TEST_SIZE)])
    print("OK" if search_OK else "NOT OK")

    return insert_OK and remove_OK and search_OK


if __name__ == "__main__":
    print("Skip list tests")

    print("Good job" if run_all_tests() else "Sorry")
    


