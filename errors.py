import numpy as np
from error_abstract import Error_abstr


class Errors(Error_abstr):
    def __init__(self, NUMBERS):
        self.NUMBERS = NUMBERS

    # The local truncation error of the Euler method is the difference
    # between the numerical solution after one step, y1
    # and the exact solution at time t1=t0+h
    # in fact,we have already counted exact and numerical solution
    # so we can count their difference in points
    def local_error(self, y_graph, y_number_method):
        f = np.zeros([self.NUMBERS])
        for i in range(self.NUMBERS):
            f[i] = abs(y_graph[i] - y_number_method[i])
        return f
