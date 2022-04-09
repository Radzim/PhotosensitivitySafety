import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation


class Register:
    def __init__(self):
        self.values = {}

    def add(self, name, x):
        if name in self.values.keys():
            self.values[name].append(x)
        else:
            self.values[name] = [x]

    def get(self, name):
        return self.values[name]

    def plot(self):
        fig, axs = plt.subplots(len(self.values.keys()))
        titles = list(self.values.keys())
        for i in range(len(titles)):
            axs[i].plot(np.arange(len(self.values[titles[i]])), self.values[titles[i]])
            axs[i].set_title(titles[i])
        fig.tight_layout()
        plt.show()

