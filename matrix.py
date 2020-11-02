# Dallin Dmytryk 2020/07/29
# Sudoku solver and representation
from __future__ import unicode_literals, print_function
from prompt_toolkit import print_formatted_text, HTML
from fraction import Fraction


class Matrix:

    def __init__(self, rows, columns, equation=False):
        self.rows = rows
        self.cols = columns
        self.board = []
        for row in range(1, rows + 1):
            newRow = []
            for column in range(1, columns + 1):
                if equation:
                    newRow.append(equation(row, column))
                else:
                    newRow.append(Fraction(0))
            self.board.append(newRow)

    def square(self):
        return self.cols == self.rows

    def symmetric(self):
        if not self.square():
            print("not square")
            return False
        temp = self.copy()
        temp.transpose()
        m1Elements = self.allElements()
        m2Elements = temp.allElements()
        for element in range(len(m1Elements)):
            if not m1Elements[element].equal(m2Elements[element]):
                return False
        return True

    def column(self, col):
        # returns a list of a single column of the board
        assert col <= self.cols and col > 0, "column out of range"
        return [self.board[row][col - 1] for row in range(self.rows)]

    def allColumns(self):
        # returns a list of all columns
        return [self.column(x + 1) for x in range(self.cols)]

    def row(self, row):
        # returns a list of a single row of the board
        assert row <= self.rows and row > 0, "row out of range"
        return self.board[row - 1]

    def allRows(self):
        # returns a list of all rows
        return [self.row(row + 1) for row in range(self.rows)]

    def element(self, row, column):
        assert row <= self.rows and row > 0, "row out of range"
        assert col <= self.cols and col > 0, "column out of range"
        return self.board[row - 1][column - 1]

    def allElements(self):
        elems = []
        for row in self.allRows():
            elems += row
        return elems

    def columnWidth(self):
        length = 0
        for element in self.allElements():
            length = max(length, element.length())
        return length

    def scalarMultiply(self, term):
        assert isinstance(term, int) or isinstance(
            term, Fraction), "Wrong type"
        for element in self.allElements():
            element.multiply(term)

    def rowMultiply(self, row, term):
        assert row <= self.rows and row > 0, "row out of range"
        assert isinstance(term, int) or isinstance(
            term, Fraction), "Wrong type"
        for element in self.row(row):
            element.multiply(term)

    def rowSwap(self, row1, row2):
        assert row <= self.rows and row > 0, "row out of range"
        assert row2 <= self.rows and row2 > 0, "row out of range"
        temp = self.row(row1)
        self.board[row1 - 1] = self.row(row2)
        self.board[row2 - 1] = temp

    def rowAdd(self, row1, row2, factor):
        assert row <= self.rows and row > 0, "row out of range"
        assert row2 <= self.rows and row2 > 0, "row out of range"
        assert isinstance(factor, int) or isinstance(
            factor, Fraction), "Wrong type"
        for entry in range(self.cols):
            copy = self.row(row2)[entry].copy()
            copy.multiply(factor)
            self.row(row1)[entry].add(copy)

    def rowSubtract(self, row1, row2, factor):
        assert row1 <= self.rows and row1 > 0, "row out of range"
        assert row2 <= self.rows and row2 > 0, "row out of range"
        assert isinstance(factor, int) or isinstance(
            factor, Fraction), "Wrong type"
        for entry in range(self.cols):
            copy = self.row(row2)[entry].copy()
            copy.multiply(factor)
            self.row(row1)[entry].subtract(copy)

    def matrixMultply(self, matrix):
        assert isinstance(matrix, Matrix), "Wrong type"
        assert self.cols == matrix.rows, "Size mismatch"
        temp = Matrix(self.rows, matrix.cols)
        for row in range(1, self.rows + 1):
            for column in range(1, matrix.cols + 1):
                term1 = self.row(row)
                term2 = matrix.column(column)
                product = self.vectorMultiply(term1, term2)
                temp.board[row - 1][column - 1] = product
        return temp

    def vectorMultiply(self, v1, v2):
        assert len(v1) == len(v2), "Size mismatch"
        total = Fraction(0)
        for element in range(len(v1)):
            product = v1[element].copy()
            product.multiply(v2[element])

            total.add(product)
        return total

    def matrixAdd(self, matrix):
        assert isinstance(matrix, Matrix), "Wrong type"
        assert self.rows == matrix.rows
        assert self.cols == matrix.cols
        for row in range(1, self.rows + 1):
            for col in range(1, self.cols + 1):
                newEl = matrix.element(row, col)
                self.element(row, col).add(newEl)

    def matrixSubtract(self, matrix):
        assert isinstance(matrix, Matrix), "Wrong type"
        assert self.rows == matrix.rows
        assert self.cols == matrix.cols
        for row in range(1, self.rows + 1):
            for col in range(1, self.cols + 1):
                newEl = matrix.element(row, col)
                self.element(row, col).subtract(newEl)

    def transpose(self):
        newBoard = []
        for col in self.allColumns():
            newBoard.append(col)
        temp = self.cols
        self.cols = self.rows
        self.rows = temp
        self.board = newBoard

    def echelon(self):
        for row in range(1, self.rows + 1):
            self.cascade()
            self.leading1(row)
            for row2 in range(row + 1, self.rows + 1):
                leading = self.leftEnrty(row)
                factor = self.row(row2)[leading - 1].copy()
                self.rowSubtract(row2, row, factor)

    def rowReducedEchelon(self):
        for row in range(1, self.rows + 1):
            self.cascade()
            self.leading1(row)
            for row2 in range(row + 1, self.rows + 1):
                leading = self.leftEnrty(row)
                factor = self.row(row2)[leading - 1].copy()
                self.rowSubtract(row2, row, factor)
            for row2 in range(row - 1, 0, -1):
                leading = self.leftEnrty(row)
                factor = self.row(row2)[leading - 1].copy()
                self.rowSubtract(row2, row, factor)

    def leading1(self, row):
        assert row <= self.rows and row > 0, "row out of range"
        for element in self.row(row):
            if element.non0():
                inverse = element.copy()
                inverse.inverse()
                self.rowMultiply(row, inverse)
                break

    def leftEnrty(self, row):
        assert row <= self.rows and row > 0, "row out of range"
        for entry in range(self.cols):
            if self.board[row - 1][entry].non0():
                return entry + 1
        return 0

    def cascade(self):
        changeMade = True
        while changeMade:
            changeMade = False
            for row in range(1, self.rows):
                leftEnrty = self.leftEnrty(row + 1)
                if self.leftEnrty(row) > leftEnrty and leftEnrty:
                    self.rowSwap(row, row + 1)
                    changeMade = True

    def copy(self):
        newMatrix = Matrix(self.rows, self.cols)
        for row in range(self.rows):
            for column in range(self.cols):
                newMatrix.board[row][column] = self.board[row][column].copy()
        return newMatrix

    def print(self):
        # displays the matrix
        width = self.columnWidth()
        print("_" * (self.cols * (width + 1) + 1))
        for row in self.allRows():
            printRow = "|"
            for element in row:
                printRow += str(element).center(width) + "|"
            print_formatted_text(HTML('<u>' + printRow + '</u>'))

    def __repr__(self):
        # displays the matrix
        width = self.columnWidth()
        printString = "-" * (self.cols * (width + 1) + 1) + "\n"
        for row in self.allRows():
            printRow = "|"
            for element in row:
                printRow += str(element).rjust(width) + "|"
            printString += printRow + "\n"
            printString += "-" * (self.cols * (width + 1) + 1) + "\n"
        return printString


if __name__ == "__main__":
    def eq(row, column): return Fraction(row+column)

    def eq2(row, column): return Fraction(row, column)
    matrix = Matrix(4, 4, eq)
    matrix2 = matrix.copy()
    matrix2.rowReducedEchelon()
    print(matrix)
    print(matrix2)
