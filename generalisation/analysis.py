from cv2 import cv2
from GitHub.generalisation.libraries import register


class Guideline:
    def __init__(self, pipeline): #, display):
        self.pipeline = pipeline
        #self.display = display

    # def set_display(self, size, ...):
    #     # analyse at 1' viewing distance pixels
    #     # analyse at 10' size and do shit

    def analyse(self, path):
        capture = cv2.VideoCapture(path)
        # frame_rate =
        values = register.Register()
        while True:
            check, frame = capture.read()
            if not check:
                break
            self.pipeline(frame, values)
            # self.pipeline(self.display(frame), values)
        values.plot()
        return values.values


"""
Exception: Flashing that is a fine, balanced, pattern such as white noise or an alternating checkerboard pattern with 
"squares" smaller than 0.1 degree (of visual field at typical viewing distance) on a side does not violate the 
thresholds. 
"""

"""For general software or Web content, using a 341 x 256 pixel rectangle anywhere on the displayed screen area when 
the content is viewed at 1024 x 768 pixels will provide a good estimate of a 10 degree visual field for standard 
screen sizes and viewing distances (e.g., 15-17 inch screen at 22-26 inches). """


# display_properties = {'width': 1024, 'height': 768, 'size': 16, 'distance': 24}
# # TODO: "10 degree visual field on the screen"
# frame_shape = (display_properties['width'], display_properties['height'])
# # TODO: first, make this fullHD
# # TODO: second, carefully resize first
# # frame_shape = (480, 320)
# visual_field = (341, 256)
#
# # "25% of any 10 degree visual field on the screen"
# # regional_threshold = 0.25
# # if below global_minimum_threshold there cannot be any rectangles
# # global_minimum_threshold = 0.25 / (frame_shape[0] * frame_shape[1] / visual_field[0] / visual_field[1])