from cv2 import cv2
from GitHub.generalisation.libraries import register


class Guideline:
    def __init__(self, function_objects, pipeline):
        self.function_objects = function_objects
        self.pipeline = pipeline

    def analyse(self, path):
        capture = cv2.VideoCapture(path)
        values = register.Register()
        while True:
            check, frame = capture.read()
            if not check:
                break
            self.pipeline(frame, values)
        values.plot()
        return values.values
