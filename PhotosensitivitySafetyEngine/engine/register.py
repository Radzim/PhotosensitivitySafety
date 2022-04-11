import numpy as np
from matplotlib import pyplot as plt


class Register:
    def __init__(self):
        self.values = {}
        self.figure = None

    def add(self, name, x):
        if name in self.values.keys():
            self.values[name].append(x)
        else:
            self.values[name] = [x]

    def add_all(self, pipeline, values):
        for i in range(len(pipeline)):
            if len(pipeline[i]) > 2:
                self.add(pipeline[i][2], values[i+1])

    def get(self, name):
        return self.values[name]

    def plot(self):
        plt.ioff()
        plt.close('all')
        fig, axs = plt.subplots(len(self.values.keys()))
        titles = list(self.values.keys())
        for i in range(len(titles)):
            axs[i].plot(np.arange(len(self.values[titles[i]])), self.values[titles[i]])
            axs[i].set_title(titles[i])
        fig.canvas.manager.set_window_title('Analysis Results')
        fig.tight_layout()
        plt.show()

    def live_plot(self):
        if self.figure is None:
            plt.ion()
            fig, axs = plt.subplots(len(self.values.keys()))
            titles = list(self.values.keys())
            lin = []
            for i in range(len(titles)):
                axs[i].set_title(titles[i])
                line, = axs[i].plot(np.arange(len(self.values[titles[i]])), self.values[titles[i]])
                lin.append(line)
            self.figure = fig, axs, lin
            fig.canvas.manager.set_window_title('Live Analysis')
            plt.tight_layout()
        fig, axs, lin = self.figure
        titles = list(self.values.keys())
        for i in range(len(titles)):
            lin[i].set_xdata(np.arange(len(self.values[titles[i]])))
            lin[i].set_ydata(self.values[titles[i]])
            axs[i].relim()
            axs[i].autoscale_view(True, True, True)
        fig.canvas.draw()
        fig.canvas.flush_events()