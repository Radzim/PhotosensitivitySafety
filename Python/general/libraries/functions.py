import numpy as np

from GitHub.Python.general.lambdas import *


def colorCurve(fun=None, curve=None, fromRGB=False):
    curves = {
        'RGB2sRGB': lambda X: X / 255,
        'RGB2XYZ': lambda X: ((X / 255 + 0.055) / 1.055) ** 2.4 if X / 255 > 0.03928 else X / 255 / 12.92
    }
    if fromRGB:
        if fun is not None:
            return InputToArray(fun)
        if curve is not None:
            return InputToArray(curves[curve])
    else:
        if fun is not None:
            return ArrayToArray(fun)
        if curve is not None:
            return ArrayToArray(curves[curve])


def relativeLuminance(fromRGB=False):
    # if fromRGB:
    #     Compose(colorCurve(curve='RGB2XYZ').run())
    return ArrayToArrayChannels(lambda R, G, B: 0.2126 * R + 0.7152 * G + 0.0722 * B, vector_form=True)

#
# lighter = ArrayAndPastToArray(lambda Present, Past:  np.where(Present - Past >= 0.1, 1, 0) * np.where(Past <= 0.8, 1, 0), vector_form=True)
# darker = ArrayAndPastToArray(lambda Present, Past:  np.where(Past - Present >= 0.1, 1, 0) * np.where(Present <= 0.8, 1, 0), vector_form=True)
# maximumRegion = ArrayToBoolean(lambda x: custom.area_averages_max(x, threshold=0.25))
# redSaturation = ArrayToArrayChannels(lambda R, G, B: np.divide(R, (R + G + B), out=np.zeros(R.shape, dtype=float), where=R != 0), vector_form=True)
# redMajority = ArrayToArrayChannels(lambda R, G, B: np.maximum(R - G - B, 0) * 320, vector_form=True)
# redMajorityChangeUp = ArrayAndPastToArray(lambda Present, Past: np.where(Present - Past > 20, 1, 0), vector_form=True)
# redMajorityChangeDown = ArrayAndPastToArray(lambda Present, Past: np.where(Past - Present > 20, 1, 0), vector_form=True)
# redSaturationChange = ArrayAndPastToArray(lambda Present, Past: np.maximum(Present, Past) >= 0.8, vector_form=True)
# bothConditions = ArraysToArray(lambda Array1, Array2: np.logical_and(Array1, Array2), vector_form=True)
