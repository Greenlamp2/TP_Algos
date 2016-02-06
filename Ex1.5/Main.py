import re

def check_line(line):
    rules = {
        "(" : ")",
        "[" : "]",
        "{" : "}"
    }

    opening = []
    closing = []
    for i in range(len(line)):
        if(line[i] in rules):
            opening.append(line[i])
            closing.append(rules[line[i]])
        elif(line[i] in closing):
            closing_attended = rules[opening[-1]]
            if(closing_attended == line[i]):
                closing.remove(closing[-1])
                opening.remove(opening[-1])


    return len(opening) == 0


if __name__ == "__main__":
    character = None
    line = ""
    while(character != "#"):
        print("enter a letter and exit with a #")
        character = input()
        line = line + character

    #line = "a(b{c})"
    #line = "a(b{c})"

    if(check_line(line)):
        print(line + " is ok with the rules")
    else:
        print(line + " is not ok with the rules")

