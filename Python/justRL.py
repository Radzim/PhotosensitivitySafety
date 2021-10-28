import pafy
import plot
from frame_functions import *
from help_functions import *

# SETTINGS
videoPick = 5
displayAnalysis = True

# INITIALISE
luminancePlot = plot.Plotter(500, 300)
luminanceLimitPlotLighter = plot.Plotter(500, 300)
luminanceLimitPlotDarker = plot.Plotter(500, 300)
redLimitPlot = plot.Plotter(500, 300)

previousDisplayFrame = 0
previousRelativeLuminance = 0.0
previousRedMajority = 0.0
previousRedSaturation = 0.0
lastChanges = (0.0, 0.0)

frameCount = 0
frameRate = 24

# THRESHOLDS
thresholds = 0.25/9, 0.25  # 2.8%, 25.0%

# VIDEO LIST
videos = [
    ("https://www.youtube.com/watch?v=GuLcxg5VGuo", 'pafy'),  # barney video cv
    ("https://www.youtube.com/watch?v=B4wSFjR9TMQ", 'pafy'),  # pokemon
    ("https://www.youtube.com/watch?v=FkhfLNfWIHA", 'pafy'),  # flashing images
    ("https://www.youtube.com/watch?v=XqZsoesa55w", 'pafy'),  # baby shark
    ("https://www.youtube.com/watch?v=0EqSXDwTq6U", 'pafy'),  # charlie bit my finger
    ('C:/Users/radzi/OneDrive/Desktop/Project/Media/Pokemon.mp4', 'local')  # pokemon local
]
video = videos[videoPick]

# SET VIDEO CAPTURE
if video[1] == 'pafy':
    capture = cv2.VideoCapture(pafy.new(video[0]).getbest(preftype="mp4").url)
else:
    capture = cv2.VideoCapture(video[0])

while True:

    frameCount += 1

    check, frame = capture.read()

    if check:

        # CALCULATIONS
        frameWithoutArtifacts = cv2.resize(frame, (300, 225))
        relativeLuminance = calculate_relative_luminance(frameWithoutArtifacts)
        relativeLuminanceLimits = relative_luminance_both_limits(relativeLuminance, previousRelativeLuminance)
        lastChanges = update_both_last_flashes(lastChanges, relativeLuminanceLimits, frameRate)
        flashes = cross_reference_both_transitions(lastChanges, relativeLuminanceLimits)
        flashCounts = flash_both_frames_separator(flashes)
        flashFlag = flash_detect_printout_both(flashCounts, frameCount, frameRate, thresholds)

        # DISPLAY ANALYSIS
        if displayAnalysis:
            # SHOW VIDEOS
            display_content(frameWithoutArtifacts, max_value=255)
            display_content(relativeLuminance)
            display_content(relativeLuminanceLimits[0])
            display_content(relativeLuminanceLimits[1])
            display_content(lastChanges[0], max_value=frameRate)
            display_content(lastChanges[1], max_value=frameRate)
            display_content(flashes[0], max_value=frameRate)
            display_content(flashes[1], max_value=frameRate)

            # SHOW PLOTS

            # WAIT
            cv2.waitKey(10)

        # REMEMBER LAST FRAME
        previousRelativeLuminance = relativeLuminance

        continue
    break

# END CAPTURE AND MONITORS
capture.release()
cv2.destroyAllWindows()
