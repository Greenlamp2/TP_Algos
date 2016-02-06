import re

if __name__ == "__main__":
    character = None
    line = ""
    while(character != "#"):
        print("enter a letter and exit with a #")
        character = input()
        line = line + character
        left = re.search('(.*)\*', line)
        right = re.search('\*(.*)#', line)
        if(right != None):
            if(left.group(1) == right.group(1)[::-1]):
                print(line + " is ok with the rule")
            else:
                print(line + " is not ok with the rule")