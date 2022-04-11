import numpy as np
from cv2 import cv2
import math
from GitHub.generalisation import register


class GuidelineProcess:
    def __init__(self, objects, pipeline):
        self.objects = objects
        self.pipeline = pipeline

        self.display_properties = {
            'frame_rate': 30,
            'analysis_size': (341, 256),
            'one_degree_field': (0.033, 0.033),
            'ten_degree_field': (0.33, 0.33)
        }
        self.display_function = lambda frame: render_onto_display(frame, display_size=self.display_properties['analysis_size'])

    def set_physical_display(self, display_size, display_diameter_cm=None, display_distance_cm=None):
        if display_diameter_cm is not None and display_distance_cm is not None:
            pixels_per_cm = (display_size[0]**2+display_size[1]**2)**0.5/display_diameter_cm
            one_degree_pixels = math.sin(math.pi/180)*display_distance_cm*pixels_per_cm
            self.display_properties['one_degree_field'] = (10*one_degree_pixels/display_size[0], 10*one_degree_pixels/display_size[1])
        # self.display_properties['analysis_size'] = (int(display_size[0] / (self.display_properties['one_degree_field'][0]/10)), int(display_size[1] / (self.display_properties['one_degree_field'][1]/10)))
        self.display_function = lambda frame: render_onto_display(frame, display_size=self.display_properties['analysis_size'])

    def analyse(self, path):
        capture = cv2.VideoCapture(path)
        self.display_properties['frame_rate'] = int(capture.get(cv2.CAP_PROP_FPS))
        objects_with_properties = self.objects(self.display_properties)
        value_register = register.Register()
        while True:
            check, frame = capture.read()
            if not check:
                break
            # FRAME PROCESSING
            frame = self.display_function(frame)
            display_content(frame, max_value=255)
            # PIPELINE
            values = [frame]
            for (fun, xs, *_) in self.pipeline:
                values.append(objects_with_properties[fun].run(*[values[x] for x in xs] if type(xs) is tuple else [values[xs]]))
            # CHART VALUES
            for i in range(len(self.pipeline)):
                if len(self.pipeline[i]) > 2:
                    value_register.add(self.pipeline[i][2], values[i+1])
            value_register.live_plot()
        value_register.plot()
        return





















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
