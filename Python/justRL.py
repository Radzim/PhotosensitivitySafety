import cv2
import numpy as np
import pafy
import plot

# SETTINGS
videoPick = 0
displayAnalysis = True

# INITIALISE
luminancePlot = plot.Plotter(500, 300)
luminanceLimitPlotLighter = plot.Plotter(500, 300)
luminanceLimitPlotDarker = plot.Plotter(500, 300)
redLimitPlot = plot.Plotter(500, 300)

previousRelativeLuminance = 0
previousRedMajority = 0
previousRedSaturation = 0

# VIDEO LIST
videos = [
    ("https://www.youtube.com/watch?v=GuLcxg5VGuo", 'pafy'),  # barney video cv
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

        # SHOW MONITORS
        if displayAnalysis:

            # SHOW VIDEOS

            cv2.imshow('Original', X8bit)

            limitRelativeLuminance8bitLighter = np.array(np.multiply(limitRelativeLuminanceLighter, 255), dtype=np.uint8)
            cv2.imshow('Lighter Relative Luminance Delta Breach', limitRelativeLuminance8bitLighter)
            limitRelativeLuminance8bitDarker = np.array(np.multiply(limitRelativeLuminanceDarker, 255), dtype=np.uint8)
            cv2.imshow('Darker Relative Luminance Delta Breach', limitRelativeLuminance8bitDarker)

            # SHOW PLOTS

            luminanceLimitPlotDarker.plot(np.average(limitRelativeLuminance8bitDarker), label="Darker", line=0)
            luminanceLimitPlotLighter.plot(np.average(limitRelativeLuminance8bitLighter), label="Lighter", line=0)

            cv2.waitKey(10)

        # REMEMBER LAST FRAME

        previousRelativeLuminance = relativeLuminance

        continue
    break

# END CAPTURE AND MONITORS

capture.release()

cv2.destroyAllWindows()
