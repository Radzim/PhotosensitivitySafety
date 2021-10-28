import cv2
import pafy
import plot
from functions import *

# SETTINGS
videoPick = 5
displayAnalysis = False

# INITIALISE
luminancePlot = plot.Plotter(500, 300)
luminanceLimitPlotLighter = plot.Plotter(500, 300)
luminanceLimitPlotDarker = plot.Plotter(500, 300)
redLimitPlot = plot.Plotter(500, 300)

previousRelativeLuminance = 0.0
previousRedMajority = 0.0
previousRedSaturation = 0.0
lastChanges = (0.0, 0.0)

frameCount = 0
frameRate = 24

# THRESHOLDS
globalMaxThreshold = 0.25  # 25%
globalMinThreshold = 1 / 9 * globalMaxThreshold  # 2.8%
thresholds = globalMinThreshold, globalMaxThreshold

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

        X8bit = cv2.resize(frame, (300, 225))

        relativeLuminance = calculate_relative_luminance(X8bit)
        relativeLuminanceLimits = relative_luminance_both_limits(relativeLuminance, previousRelativeLuminance)
        lastChanges = update_both_last_flashes(lastChanges, relativeLuminanceLimits, frameRate)
        flashes = cross_reference_both_transitions(lastChanges, relativeLuminanceLimits)
        flash_counts = flash_both_frames_separator(flashes)
        flash_detect_printout_both(flash_counts, frameCount, frameRate, thresholds)

        # SHOW MONITORS
        if displayAnalysis:

            # SHOW VIDEOS

            cv2.imshow('Original', X8bit)

            limitRelativeLuminanceLighter8bit = np.array(np.multiply(limitRelativeLuminanceLighter, 255), dtype=np.uint8)
            cv2.imshow('Lighter Relative Luminance Delta Breach', limitRelativeLuminanceLighter8bit)
            limitRelativeLuminanceDarker8bit = np.array(np.multiply(limitRelativeLuminanceDarker, 255), dtype=np.uint8)
            cv2.imshow('Darker Relative Luminance Delta Breach', limitRelativeLuminanceDarker8bit)

            lastLighter8bit = np.array(np.multiply(lastLighter, 10), dtype=np.uint8)
            cv2.imshow('LastLighter', lastLighter8bit)
            lastDarker8bit = np.array(np.multiply(lastDarker, 10), dtype=np.uint8)
            cv2.imshow('LastDarker', lastDarker8bit)

            lighterDarkerFlash8bit = np.array(np.multiply(lighterDarkerFlash, 10), dtype=np.uint8)
            cv2.imshow('Lighter-Darker Flash', lighterDarkerFlash8bit)
            darkerLighterFlash8bit = np.array(np.multiply(darkerLighterFlash, 10), dtype=np.uint8)
            cv2.imshow('Darker-Lighter Flash', darkerLighterFlash8bit)

            # regionalLimitRelativeLuminance8bitLighter = np.array(np.multiply(regionalLimitRelativeLuminanceLighter, 255), dtype=np.uint8)
            # cv2.imshow('Regional Lighter Relative Luminance Delta Breach', cv2.resize(regionalLimitRelativeLuminance8bitLighter, (200, 150), interpolation=cv2.INTER_NEAREST))
            # regionalLimitRelativeLuminance8bitDarker = np.array(np.multiply(regionalLimitRelativeLuminanceDarker, 255), dtype=np.uint8)
            # cv2.imshow('Regional Darker Relative Luminance Delta Breach', cv2.resize(regionalLimitRelativeLuminance8bitDarker, (200, 150), interpolation=cv2.INTER_NEAREST))

            # SHOW PLOTS

            luminanceLimitPlotDarker.plot(np.average(limitRelativeLuminanceDarker8bit), label="Darker", line=0)
            luminanceLimitPlotLighter.plot(np.average(limitRelativeLuminanceLighter8bit), label="Lighter", line=0)

            cv2.waitKey(10)

        # REMEMBER LAST FRAME

        previousRelativeLuminance = relativeLuminance

        continue
    break

# END CAPTURE AND MONITORS

capture.release()

cv2.destroyAllWindows()
