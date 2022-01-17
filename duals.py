"""Class to demonstrate the power of duals"""


class Dual:
    """Class to implement Duals. For more information, see https://en.wikipedia.org/wiki/Dual_number"""

    def __init__(self, real_part, dual_part):
        self.real_part = real_part
        self.dual_part = dual_part

    def __add__(self, other):
        if isinstance(other, Dual):
            return Dual(
                self.real_part + other.real_part, self.dual_part + other.dual_part
            )
        if isinstance(other, (int, float)):
            # Just assume that they only want the real_part
            return Dual(self.real_part + other, self.dual_part)
        return NotImplementedError(
            f"{type(other).__name__} type not defined for addition with duals"
        )

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Dual):
            return Dual(
                self.real_part - other.real_part, self.dual_part - other.dual_part
            )
        if isinstance(other, (int, float)):
            return Dual(self.real_part - other, self.dual_part)
        return NotImplementedError(
            f"{type(other).__name__} type not defined for subtraction with duals"
        )

    __rsub__ = __sub__

    def __mul__(self, other):
        # Check if it's a dual, otherwise handle it like normal scalar operation
        # If it's not a number, raise.
        if isinstance(other, Dual):
            # Foil baby
            # (a + b\eps) * (c + d\eps) = (a*c) + (c*b\eps) + (a*d\eps) + (b*d)(\eps)**2
            # But oh snap! Apply \eps**2 == 0
            # (a*c) + (c*b\eps) + (a*d\eps)
            return Dual(
                self.real_part * other.real_part, self.dual_part + other.dual_part
            )
        if isinstance(other, (int, float)):
            return Dual(self.real_part * other, self.dual_part * other)
        return NotImplementedError(
            f"{type(other).__name__} type not defined for multiplciation with duals"
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, Dual):
            dual_numerator = (
                self.dual_part * other.real_part - other.dual_part * self.real_part
            )
            dual_denominator = other.real_part ** 2
            return Dual(
                self.real_part / other.real_part, dual_numerator / dual_denominator
            )
        if isinstance(other, (int, float)):
            return Dual(self.real_part / other, self.dual_part)
        return NotImplementedError(
            f"{type(other).__name__} type not defined for division with duals"
        )

    def __rdiv__(self, other):
        if isinstance(other, Dual):
            return other.__truediv__(self)
        if isinstance(other, (int, float)):
            return Dual(other / self.real_part, 1 / self.dual_part)
        return NotImplementedError(
            f"{type(other).__name__} type not defined for division with duals"
        )

    def __pow__(self, other):
        # Just take into account the binomail expansion
        # but the beauty is we only need to worry about the first two terms.
        # Only works for numbers... don't wanna think about raising a dual to a dual
        if isinstance(other, (int, float)):
            return Dual(
                self.real_part ** other,
                other * self.dual_part * (self.real_part ** (other - 1)),
            )
        return NotImplementedError(
            f"{type(other).__name__} not defined for power with duals. Only int/float"
        )

    def __str__(self) -> str:
        return f"({self.real_part}, {self.dual_part}\u03B5)"

    def __repr__(self) -> str:
        return self.__str__()


def value_and_derivative_at_point(function_to_eval, point):
    """Wrapper around function to invoke and print helpful dual results"""
    result = function_to_eval.function(Dual(point, 1))
    value, deriv = result.real_part, result.dual_part
    print(f"For function {function_to_eval}, f({point})={value}, f'({point})={deriv}")
    return value, deriv


class GeneralFunction:
    """Abusing eval so we can see our function definition"""
    def __init__(self, definition):
        self.definition = definition

    def __str__(self):
        return self.definition

    def function(self, x):
        """Evaluate our expression. Note, x (arg1) is used in the expression."""
        return eval(self.definition)


if __name__ == "__main__":
    x = Dual(4, 3)
    y = Dual(5, 7)
    print(f"x: {x}")
    print(f"y: {y}")
    print(f"x + y : {x + y}")
    print(f"y + x : {y + x}")
    print(f"x * y : {x * y}")
    print(f"y * x : {y * x}")
    print(f"x - y : {x - y}")
    print(f"y - x : {y - x}")
    print(f"x / y : {x / y}")
    print(f"y / x : {y / x}")

    func = GeneralFunction("x**2 + 7*x - 18")
    value_and_derivative_at_point(func, 7)
