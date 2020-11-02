# class to represent fractions in the form int/int
from math import isqrt


class Fraction:

    def __init__(self, numerator, denominater=1):
        self.numerator = numerator
        self.denominater = denominater
        self.sign = 1
        self.reduce()

    def equal(self, term):
        if isinstance(term, int):
            return self.denominater == 1 and self.numerator == term
        elif isinstance(term, Fraction):
            return (self.numerator == term.numerator
                    and self.denominater == term.denominater
                    and self.sign == term.sign)
        return False

    def reduce(self):
        # reduce sign
        if (self.numerator < 0):
            self.numerator *= -1
            self.sign *= -1
        if (self.denominater < 0):
            self.denominater *= -1
            self.sign *= -1
        # reduce common factors
        bound = min(self.numerator, self.denominater)
        factor = 2
        while (factor <= bound):
            if (not self.numerator % factor and not self.denominater % factor):
                self.numerator //= factor
                self.denominater //= factor
            else:
                factor += 1
        # reduce 0 factors
        if (self.numerator == 0 or self.denominater == 0):
            self.numerator = 0
            self.denominater = 0
            self.sign = 1

    def length(self):
        length = 0
        if (self.sign < 0):
            length += 1
        length += len(str(self.numerator))
        if (not self.whole()):
            length += len(str(self.denominater)) + 1
        return length

    def whole(self):
        return self.denominater == 1 or self.denominater == 0

    def non0(self):
        return self.numerator != 0

    def power(self, pow):
        assert isinstance(pow, int)
        self.numerator = self.numerator**pow
        self.denominater = self.denominater**pow
        self.sign = self.sign**pow
        self.reduce()

    def inverse(self):
        temp = self.numerator
        self.numerator = self.denominater
        self.denominater = temp

    def multiply(self, term):
        if (isinstance(term, int)):
            self.numerator *= term
        elif (isinstance(term, Fraction)):
            self.numerator *= term.numerator
            self.denominater *= term.denominater
            self.sign *= term.sign
        self.reduce()

    def divide(self, term):
        if (isinstance(term, int)):
            self.denominater *= term
        elif (isinstance(term, Fraction)):
            inverse = term.copy()
            inverse.inverse()
            self.multiply(inverse)
        self.reduce()

    def add(self, term):
        if (isinstance(term, int)):
            if self.numerator:
                self.numerator += term * self.denominater * self.sign
            else:
                self.numerator += term * self.sign
                self.denominater = 1
        elif (isinstance(term, Fraction)):
            if (self.denominater and term.denominater):
                temp = self.denominater
                self.numerator *= term.denominater
                self.denominater *= term.denominater
                self.numerator += term.numerator * self.sign * temp * term.sign
            else:
                self.denominater += term.denominater
                self.numerator += term.numerator * self.sign * term.sign
        self.reduce()

    def subtract(self, term):
        if (isinstance(term, int)):
            self.add(-1 * term)
        elif (isinstance(term, Fraction)):
            self.add(Fraction(term.sign * -term.numerator, term.denominater))
        self.reduce()

    def copy(self):
        return Fraction(self.numerator * self.sign, self.denominater)

    def __str__(self):
        if (self.sign < 0):
            sign = "-"
        else:
            sign = ""
        if (self.whole()):
            return sign + str(self.numerator)
        else:
            return "{}{}/{}".format(sign, self.numerator, self.denominater)

    def __repr__(self):
        if (self.sign < 0):
            sign = "-"
        else:
            sign = ""
        if (self.whole()):
            return sign + str(self.numerator)
        else:
            return "{}{}/{}".format(sign, self.numerator, self.denominater)


if __name__ == "__main__":
    fraction = Fraction(1, 3)
    fraction2 = Fraction(1, 3)
    print(fraction, fraction2)
    fraction.divide(fraction2)
    print(fraction)
