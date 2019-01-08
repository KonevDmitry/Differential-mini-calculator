import sympy as sy
import re
from fractions import Fraction
import numpy as np
from exact_abstract import Graph_abstr

"""checking for working with float numbers"""


def is_float(string):
    if string.isdigit():
        return True
    else:
        try:
            float(Fraction(string))
            return True
        except ValueError:
            return False


class Graph(Graph_abstr):
    def __init__(self, x0, y0, X, NUMBERS):
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.NUMBERS = NUMBERS

    def solve(self):
        # sin(x)+y=y'
        # y=(3/2)*np.exp(x)-np.sin(x)/2-np.cos(x)/2 - solution with IVP
        f_x = sy.Symbol('x')
        f_y = sy.Function('y')
        # f_eq = sy.Eq(f_y(f_x).diff(f_x) - f_y(f_x), sy.sin(f_x))
        # f_sol = sy.dsolve(f_eq, f_y(f_x)).rhs
        # constants = sy.solve([f_sol.subs(f_x, self.x0) - self.y0], dict=True)
        f_eq = sy.Eq(f_y(f_x).diff(f_x) - f_y(f_x), sy.sin(f_x))
        f_sol = sy.dsolve(f_eq, f_y(f_x)).rhs
        constants = sy.solve([f_sol.subs(f_x, self.x0) - self.y0], dict=True)
        y = str(f_sol.subs(constants[0]))
        result = re.findall(r'\b[^\Wx]\w+', y)

        for p in range(len(result)):
            if (y.find('np.' + result[p]) == -1 and not is_float(result[p])):
                y = y.replace(result[p], 'np.' + result[p])
        x = np.linspace(self.x0, self.X, self.NUMBERS)
        fun = eval(y)
        return x, fun
