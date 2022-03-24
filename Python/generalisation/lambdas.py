from cv2 import cv2
import numpy as np
import functools
from GitHub.Python.generalisation.libraries import spaces


class InputToArray:
    def __init__(self, fun, lut=spaces.eight_bit(), vector_form=False):
        if vector_form:
            self.lut = fun(lut)
        else:
            self.lut = np.vectorize(fun)(lut)

    def run(self, array):
        return cv2.LUT(array, self.lut)


class ArrayToArray:
    def __init__(self, fun, vector_form=False):
        if vector_form:
            self.fun = fun
        else:
            self.fun = np.vectorize(fun)

    def run(self, array):
        return self.fun(array)


class ArrayToArrayChannels:
    def __init__(self, fun, vector_form=False):
        if vector_form:
            self.fun = fun
        else:
            self.fun = np.vectorize(fun)

    def run(self, array):
        b, g, r = cv2.split(array)
        return self.fun(r, g, b)


class ArraysToArray:
    def __init__(self, fun, vector_form=False):
        if vector_form:
            self.fun = fun
        else:
            self.fun = np.vectorize(fun)

    def run(self, array1, array2):
        return self.fun(array1, array2)


class ArrayAndPastToArray:
    def __init__(self, fun, vector_form=False):
        if vector_form:
            self.fun = fun
        else:
            self.fun = np.vectorize(fun)
        self.past = 0

    def run(self, array):
        ret = self.fun(array, self.past)
        self.past = array
        return ret


class ArrayToBoolean:
    def __init__(self, fun):
        self.fun = fun

    def run(self, array):
        return self.fun(array)


class Compose:
    def __init__(self, *funs):
        def compose(f, g):
            return lambda x: f(g(x))
        self.fun = functools.reduce(compose, funs, lambda x: x)

    def run(self, array):
        return self.fun(array)


class Register:
    def __init__(self):
        self.values = {}

    def add(self, x, name):
        if name in self.values.keys():
            self.values[name].append(x)
        else:
            self.values[name] = [x]

    def get(self, name):
        return self.values[name]
