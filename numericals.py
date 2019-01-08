import numpy as np
from numericals_abstract import Numerics


class Numerical_methods(Numerics):
    def __init__(self, x0, y0, X, NUMBERS):
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.NUMBERS = NUMBERS
        self.h = (X - x0) / (NUMBERS - 1)

    def euler(self):
        def __get_function(i):
            return np.sin(x[i]) + y[i]

        x = np.linspace(self.x0, self.X, self.NUMBERS)
        y = np.zeros([self.NUMBERS])
        y[0] = self.y0
        for i in range(1, self.NUMBERS):
            y[i] = y[i - 1] + self.h * __get_function(i - 1)
        return x, y

    def improved_euler(self):
        def __get_function(i):
            return np.sin(x[i]) + y[i]

        x = np.linspace(self.x0, self.X, self.NUMBERS)
        y = np.zeros([self.NUMBERS])
        y[0] = self.y0
        for i in range(1, self.NUMBERS):
            cur_x = x[i - 1] + self.h / 2
            cur_y = y[i - 1] + (self.h / 2) * __get_function(i - 1)
            y[i] = y[i - 1] + self.h * (np.sin(cur_x) + cur_y)
        return x, y

    def runge_kutta(self):
        x = np.linspace(self.x0, self.X, self.NUMBERS)
        y = np.zeros([self.NUMBERS])
        y[0] = self.y0
        for i in range(1, self.NUMBERS):
            k1 = np.sin(x[i - 1]) + y[i - 1]
            k2 = np.sin(x[i - 1] + self.h / 2) + (y[i - 1] + self.h * k1 / 2)
            k3 = np.sin(x[i - 1] + self.h / 2) + (y[i - 1] + self.h * k2 / 2)
            k4 = np.sin(x[i - 1] + self.h) + (y[i - 1] + self.h * k3)
            y[i] = y[i - 1] + (self.h / 6) * (k1 + 2 * k2 + 2 * k3 + k4);
        return x, y
