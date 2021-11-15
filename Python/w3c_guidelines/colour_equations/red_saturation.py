import numpy as np

"""
The current working definition in the field for "pair of opposing transitions involving a saturated red" is where, 
for either or both states involved in each transition, R/(R+ G + B) >= 0.8, and the change in the value of (
R-G-B)x320 is > 20 (negative values of (R-G-B)x320 are set to zero) for both transitions. R, G, B values range from 
0-1 as specified in “relative luminance” definition.
"""


def calculate_red_saturation(frame):
    # "R/(R+ G + B)"
    numerator = np.dot(frame[..., :3], [0, 0, 1])
    denominator = np.dot(frame[..., :3], [1, 1, 1])
    # note: this definition has a divide by zero problem
    red_saturation = np.divide(numerator, denominator, out=np.zeros(numerator.shape, dtype=float), where=denominator != 0)
    return red_saturation


def calculate_red_majority(frame):
    # "(R-G-B)x320"
    red_majority = np.minimum(np.multiply(np.dot(frame[..., :3], [-1, -1, 1]), 320), 0)
    return red_majority
