import numpy as np
from cv2 import cv2
import math
from GitHub.generalisation.libraries import register


class Guideline:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.display_function = render_onto_display
        self.display_properties = {
            'display_size': (1024, 768),
            'ten_degree_field': (341, 256),
            'fine_exception_speedup': 0.3
        }

    def set_physical_display(self, display_size, display_diameter_cm=None, display_distance_cm=None):
        if display_diameter_cm is not None and display_distance_cm is not None:
            pixels_per_cm = (self.display_properties['display_size'][0]**2+self.display_properties['display_size'][1]**2)**0.5/display_diameter_cm
            tenth_degree_field = math.sin(math.pi/1800)*display_distance_cm*pixels_per_cm
            ten_degrees_field = math.sin(math.pi/18)*display_distance_cm*pixels_per_cm
            self.display_properties['ten_degree_field'] = (ten_degrees_field, ten_degrees_field)
            self.display_properties['fine_exception_speedup'] = 1/tenth_degree_field
        self.display_properties['display_size'] = display_size
        self.display_function = lambda frame: render_onto_display(frame, self.display_properties['display_size'])

    def analyse(self, path):
        capture = cv2.VideoCapture(path)
        analysis_properties = {
            'frame_rate': capture.get(cv2.CAP_PROP_FPS),
        }
        values = register.Register()
        while True:
            check, frame = capture.read()
            if not check:
                break
            frame = self.display_function(frame)
            frame = cv2.resize(frame, None, fx=self.display_properties['fine_exception_speedup'], fy=self.display_properties['fine_exception_speedup'])
            display_content(frame, max_value=255)
            self.pipeline(frame, values)
        values.plot()
        return values.values


def render_onto_display(frame, display_size=(1024, 768), size=None, position=(0, 0), interpolation=cv2.INTER_LINEAR):
    screen = np.zeros((display_size[1], display_size[0], 3))
    if size is None:
        if frame.shape[0]/display_size[1] > frame.shape[1]/display_size[0]:
            size = int(frame.shape[1]/frame.shape[0]*display_size[1]), display_size[1]
            position = int((display_size[0]-size[0])/2), 0
        else:
            size = display_size[0], int(frame.shape[0]/frame.shape[1]*display_size[0])
            position = 0, int((display_size[1]-size[1])/2)
    resized_frame = cv2.resize(frame, size, interpolation=interpolation)
    screen[position[1]:position[1] + size[1], position[0]:position[0] + size[0]] = resized_frame
    return np.array(screen, dtype='uint8')


def display_content(display_frame, display_name='frame', max_value=1):
    display_frame_8bit = np.array(np.multiply(display_frame, 255 / max_value), dtype=np.uint8)
    cv2.imshow(display_name, display_frame_8bit)
    cv2.waitKey(1)
