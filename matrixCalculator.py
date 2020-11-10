import sys
from fraction import Fraction
from matrix import Matrix

objects = dict()


class Command:

    TYPES = ("help", "exit", "assign", "mMult",
             "sMult", "add", "sub", "ech", "rrEch",
             "trans", "rMult", "rSwap", "rAdd",
             "rSub", "lead1", "matrix", "object")

    def __init__(self, type, term1=None, term2=None):
        assert type in self.TYPES
        self.type = type
        self.term1 = term1
        self.term2 = term2

    def __repr__(self):
        return "{} ({}, {})".format(
            self.type, str(self.term1), str(self.term2))


def main():
    while True:

        userInput = retrive()
        command = parse(userInput)
        execute(command)


def retrive():
    # retrives user input
    userInput = input("Please enter a command, help for options: ")
    return userInput


def parse(userInput):
    # Parses input into a command to be executed
    strippedInput = userInput.lstrip()
    if strippedInput.startswith("help"):
        return Command("help")
    elif strippedInput.startswith("exit"):
        return Command("exit")
    assign = strippedInput.split("=")
    if len(assign) == 2:
        value = parse(assign[1])
        return Command("assign", assign[0].replace(" ", ""), value)
    mult = strippedInput.split(" x ")
    if len(mult) == 2 and " x " in strippedInput:
        m1 = parse(mult[0])
        m2 = parse(mult[1])
        return Command("mMult", m1, m2)
    if strippedInput.startswith("transpose"):
        term = parse(strippedInput.split(" ", 1)[1])
        return Command("trans", term)
    if strippedInput.startswith("rrEchelon"):
        term = parse(strippedInput.split(" ", 1)[1])
        return Command("rrEch", term)
    if strippedInput.startswith("echelon"):
        term = parse(strippedInput.split(" ", 1)[1])
        return Command("ech", term)
    if strippedInput.startswith("matrix"):
        matrix = strippedInput.split(" ", 2)
        return Command("matrix", matrix[1], matrix[2])
    for key in sorted(objects.keys(), key=lambda x: len(x), reverse=True):
        if strippedInput.startswith(key):
            return Command("object", key)
    raise Exception("Invalid command")


def execute(command):
    # Execute a command
    if command.type == "help":
        help()
    if command.type == "exit":
        sys.exit()
    if command.type == "assign":
        objects[command.term1] = execute(command.term2)
    if command.type == "mMult":
        m1 = execute(command.term1)
        m2 = execute(command.term2)
        result = m1.matrixMultply(m2)
        print(result)
        return result
    if command.type == "matrix":
        matrix = Matrix(int(command.term1), int(command.term2))
        print(
            "add elements in form int or int/int\n"
            "left to right top to bottom")
        for row in range(matrix.rows):
            for element in range(matrix.cols):
                matrix.board[row][element] = makeFraction()
        print(matrix)
        return matrix
    if command.type == "trans":
        matrix = execute(command.term1).copy()
        matrix.transpose()
        print(matrix)
        return matrix
    if command.type == "rrEch":
        matrix = execute(command.term1).copy()
        matrix.rowReducedEchelon()
        print(matrix)
        return matrix
    if command.type == "ech":
        matrix = execute(command.term1).copy()
        matrix.echelon()
        print(matrix)
        return matrix
    if command.type == "object":
        print(objects[command.term1])
        return objects[command.term1]


def help():
    helpText = (
        "Commands:\n"
        "help: displays commands\n"
        "exit: exits program\n"
        "matrix rows columns: creates a matrix\n"
        "name = value: name is assigned the value\n"
        "name: returns matrix stored in name\n"
        "transpose matrix: returns the transpose of a matrix\n"
        "echelon matrix: returns the matrix in echelon form\n"
        "rrEchelon matrix: returns the matrix in row redced echelon form"
    )
    print(helpText)


def makeFraction():
    while True:
        try:
            userInput = input()
            split = userInput.split("/")
            if len(split) == 2:
                return Fraction(int(split[0]), int(split[1]))
            else:
                return Fraction(int(userInput))
        except Exception:
            print("Invalid Input")


if __name__ == "__main__":
    main()
