import numpy as np
from cv2 import cv2
import math
from GitHub.PhotosensitivitySafetyEngine.engine import register


class GuidelineProcess:
    def __init__(self, objects, pipeline):
        self.objects = objects
        self.pipeline = pipeline

    def analyse(self, path, display=None, speedup=1):
        if display is None:
            display = Display()
        capture = cv2.VideoCapture(path)
        display.set_property('frame_rate', int(capture.get(cv2.CAP_PROP_FPS)))
        display.set_property('analysis_resolution', tuple([int(x / speedup) for x in display.get_property('display_resolution')]))
        objects_with_properties = self.objects(display.properties())
        value_register = register.Register()
        while True:
            check, frame = capture.read()
            if not check:
                break
            # PIPELINE
            values = [display.render(frame)]
            for (fun, xs, *_) in self.pipeline:
                values.append(objects_with_properties[fun].run(*[values[x] for x in xs] if type(xs) is tuple else [values[xs]]))
            # CHART VALUES
            value_register.add_all(self.pipeline, values)
            value_register.live_plot()
            cv2.imshow('Analysis', np.hstack([cv2.cvtColor(np.float32(a/np.amax(a, initial=1)), cv2.COLOR_GRAY2BGR) if a.ndim == 2 else a/np.amax(a, initial=1) for a in [x for x in values if isinstance(x, np.ndarray)]])), cv2.waitKey(1)
        cv2.destroyAllWindows()
        value_register.plot()
        return


class Display:
    def __init__(self, display_resolution=(1024, 768), display_diameter=16, display_distance=24):
        display_size = tuple([display_diameter * x1 / sum([x2 ** 2 for x2 in display_resolution]) ** 0.5 for x1 in display_resolution])
        degree_field = lambda a: tuple([math.sin(a * math.pi / 180) * display_distance / x for x in display_size])
        self.data = {
            'display_resolution': display_resolution,
            'analysis_resolution': display_resolution,
            'display_diameter': display_diameter,
            'display_distance': display_distance,
            'display_size': display_size,
            'degree_field': degree_field,
            'frame_rate': 30
        }

    def set_property(self, name, value):
        self.data[name] = value

    def get_property(self, name):
        return self.data[name]

    def properties(self):
        return self.data

    def render(self, frame):
        screen = np.zeros((self.data['analysis_resolution'][1], self.data['analysis_resolution'][0], 3))
        if frame.shape[0] / self.data['analysis_resolution'][1] > frame.shape[1] / self.data['analysis_resolution'][0]:
            size = int(frame.shape[1] / frame.shape[0] * self.data['analysis_resolution'][1]), self.data['analysis_resolution'][1]
            position = int((self.data['analysis_resolution'][0] - size[0]) / 2), 0
        else:
            size = self.data['analysis_resolution'][0], int(frame.shape[0] / frame.shape[1] * self.data['analysis_resolution'][0])
            position = 0, int((self.data['analysis_resolution'][1] - size[1]) / 2)
        resized_frame = cv2.resize(frame, size)
        screen[position[1]:position[1] + size[1], position[0]:position[0] + size[0]] = resized_frame
        return np.array(screen, dtype='uint8')
