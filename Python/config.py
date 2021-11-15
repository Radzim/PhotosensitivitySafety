from cv2 import cv2
from pafy import pafy

# SETTINGS
videoPick = 5
displayAnalysis = True
slowdown = 10

# VIDEO LIST
videos = [
    ("https://www.youtube.com/watch?v=GuLcxg5VGuo", 'pafy'),  # barney video cv
    ("https://www.youtube.com/watch?v=B4wSFjR9TMQ", 'pafy'),  # pokemon
    ("https://www.youtube.com/watch?v=FkhfLNfWIHA", 'pafy'),  # flashing images
    ("https://www.youtube.com/watch?v=XqZsoesa55w", 'pafy'),  # baby shark
    ("https://www.youtube.com/watch?v=0EqSXDwTq6U", 'pafy'),  # charlie bit my finger
    ('C:/Users/radzi/OneDrive/Desktop/Project/Media/Pokemon.mp4', 'local'),  # pokemon local
    ('C:/Users/radzi/OneDrive/Desktop/Project/Media/PEAT_1.avi', 'local'),  # peat recording local
    ('C:/Users/radzi/OneDrive/Desktop/Project/Media/video-1636024687.mp4', 'local'),  # lecture recording 1
    ('C:/Users/radzi/OneDrive/Desktop/Project/Media/video-1636024693.mp4', 'local')  # lecture recording 2
]

video = videos[videoPick]

# SET VIDEO CAPTURE
if video[1] == 'pafy':
    capture = cv2.VideoCapture(pafy.new(video[0]).getbest(preftype="mp4").url)
else:
    capture = cv2.VideoCapture(video[0])

# TODO: GET THESE AUTOMATICALLY
frame_rate = 30
analysisSize = (300, 225)
