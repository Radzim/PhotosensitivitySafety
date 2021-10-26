import cv2
import numpy as np
import pafy
import plot

# SETTINGS
videoPick = 1
displayAnalysis = True

# INITIALISE
luminancePlot = plot.Plotter(500, 300)
luminanceLimitPlotLighter = plot.Plotter(500, 300)
luminanceLimitPlotDarker = plot.Plotter(500, 300)
redLimitPlot = plot.Plotter(500, 300)

previousRelativeLuminance = 0.0
previousRedMajority = 0.0
previousRedSaturation = 0.0
lastLighter = 0.0
lastDarker = 0.0
frameCount = 0
frameRate = 24

# THRESHOLDS
globalMinimumThreshold = 1 / 9 * 0.25  # 2.8%
regions = (15, 9)
regionalThreshold = globalMinimumThreshold / (
            (regions[0] / 3 + 1) * (regions[1] / 3 + 1) / (regions[0] / 3 * 3 * regions[1] / 3 * 3))
print(globalMinimumThreshold, regionalThreshold, 1/4)

# VIDEO LIST
videos = [
    ("https://www.youtube.com/watch?v=GuLcxg5VGuo", 'pafy'),  # barney video cv
    ("https://www.youtube.com/watch?v=B4wSFjR9TMQ", 'pafy'),  # pokemon
    ("https://www.youtube.com/watch?v=FkhfLNfWIHA", 'pafy'),  # flashing images
    ("https://www.youtube.com/watch?v=XqZsoesa55w", 'pafy'),  # baby shark
    ("https://www.youtube.com/watch?v=0EqSXDwTq6U", 'pafy'),  # charlie bit my finger
    ('C:/Users/radzi/Videos/uTorrent/ted.lasso.s02e01.1080p.web.h264-glhf[eztv.re].mkv', 'local')  # ted lasso
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

        XsRGB = np.divide(np.ndarray.copy(X8bit).astype(float), 255)

        X = np.maximum(np.divide(XsRGB, 12.92), np.power(np.divide(XsRGB+0.055, 1.055), 2.4))

        relativeLuminance = np.dot(X[..., :3], [0.0722, 0.7152, 0.2126])

        deltaRelativeLuminance = relativeLuminance-previousRelativeLuminance

        limitRelativeLuminanceLighter = np.array(np.multiply(np.where(deltaRelativeLuminance >= 0.1, 1, 0), np.where(np.minimum(relativeLuminance, previousRelativeLuminance) <= 0.8, 1, 0)), dtype=np.uint8)
        limitRelativeLuminanceDarker = np.array(np.multiply(np.where(deltaRelativeLuminance <= -0.1, 1, 0), np.where(np.minimum(relativeLuminance, previousRelativeLuminance) <= 0.8, 1, 0)), dtype=np.uint8)

        lastLighter = np.maximum(np.maximum(lastLighter-1/frameRate, 0), limitRelativeLuminanceLighter)
        lastDarker = np.maximum(np.maximum(lastDarker-1/frameRate, 0), limitRelativeLuminanceDarker)
        print(np.average(lastDarker))
        # FINDING REGIONS
        # find regions of flashes!

        # Track last L and last D in matrix (frame count, frame rate maximum)
        # If L or D over threshold:
        #    Consider all 24 flashes:
        #       for each check if over 1/36 threshold
        #           if so, check rectangles (or assume for browser)!


        # some attempts to check rectangles
        # im = limitRelativeLuminanceLighter
        # M = im.shape[0] // regions[0]
        # N = im.shape[1] // regions[1]

        # tiles = [im[x:x + M, y:y + N] for x in range(0, im.shape[0], M) for y in range(0, im.shape[1], N)]
        # averages = [np.average(x) for x in tiles]

        # regionalLimitRelativeLuminanceLighter = cv2.resize(limitRelativeLuminanceLighter, regions, interpolation=cv2.INTER_LINEAR)
        # regionalLimitRelativeLuminanceDarker = cv2.resize(limitRelativeLuminanceDarker, regions, interpolation=cv2.INTER_LINEAR)

        # SHOW MONITORS
        if displayAnalysis:

            # SHOW VIDEOS

            cv2.imshow('Original', X8bit)

            limitRelativeLuminanceLighter8bit = np.array(np.multiply(limitRelativeLuminanceLighter, 255), dtype=np.uint8)
            cv2.imshow('Lighter Relative Luminance Delta Breach', limitRelativeLuminanceLighter8bit)
            limitRelativeLuminanceDarker8bit = np.array(np.multiply(limitRelativeLuminanceDarker, 255), dtype=np.uint8)
            cv2.imshow('Darker Relative Luminance Delta Breach', limitRelativeLuminanceDarker8bit)

            lastLighter8bit = np.array(np.multiply(lastLighter, 255), dtype=np.uint8)
            cv2.imshow('LastLighter', lastLighter8bit)
            lastDarker8bit = np.array(np.multiply(lastDarker, 255), dtype=np.uint8)
            cv2.imshow('LastDarker', lastDarker8bit)

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
