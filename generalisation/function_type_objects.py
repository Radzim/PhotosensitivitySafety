from cv2 import cv2
import numpy as np
import functools


class InputToArray:
    def __init__(self, fun, lut=np.arange(256), vector_form=False):
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


class ArrayToValue:
    def __init__(self, fun):
        self.fun = fun

    def run(self, array):
        return self.fun(array)


class ValueHistoryToValue:
    def __init__(self, fun):
        self.fun = fun
        self.history = []

    def run(self, value):
        self.history.append(value)
        return self.fun(self.history)


class ValueHistoriesToValue:
    def __init__(self, fun):
        self.fun = fun
        self.history1 = []
        self.history2 = []

    def run(self, value1, value2):
        self.history1.append(value1)
        self.history2.append(value2)
        return self.fun(self.history1, self.history2)


class Compose:
    def __init__(self, *functions):
        def compose(f, g):
            return lambda x: f(g(x))
        self.fun = functools.reduce(compose, functions, lambda x: x)

    def run(self, array):
        return self.fun(array)