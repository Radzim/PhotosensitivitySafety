import numpy as np


"""
general flash and red flash thresholds a flash or rapidly changing image sequence is below the threshold (i.e., 
content passes) if any of the following are true: 

there are no more than three general flashes and / or no more than three red flashes within any one-second period; 
or the combined area of flashes occurring concurrently occupies no more than a total of .006 steradians within any 10 
degree visual field on the screen (25% of any 10 degree visual field on the screen) at typical viewing distance where: 

A general flash is defined as a pair of opposing changes in relative luminance of 10% or more of the maximum relative 
luminance where the relative luminance of the darker image is below 0.80; and where "a pair of opposing changes" is 
an increase followed by a decrease, or a decrease followed by an increase, 

A red flash is defined as any pair of opposing transitions involving a saturated red 

Exception: Flashing that is a fine, balanced, pattern such as white noise or an alternating checkerboard pattern with 
"squares" smaller than 0.1 degree (of visual field at typical viewing distance) on a side does not violate the 
thresholds. 
"""


"""
The current working definition in the field for "pair of opposing transitions involving a saturated red" is where, 
for either or both states involved in each transition, R/(R+ G + B) >= 0.8, and the change in the value of (
R-G-B)x320 is > 20 (negative values of (R-G-B)x320 are set to zero) for both transitions. R, G, B values range from 
0-1 as specified in “relative luminance” definition.
"""


def red_saturation_limits(red_saturation, previous_red_saturation, red_majority, previous_red_majority):
    red_saturation_condition = red_saturation_minimum(red_saturation, previous_red_saturation)
    lighter = red_majority_limit(red_majority, previous_red_majority, red_saturation_condition, direction='lighter')
    darker = red_majority_limit(red_majority, previous_red_majority, red_saturation_condition, direction='darker')
    # "Exception: Flashing with "squares" smaller than 0.1 degree"
    # TODO: add average smoothing with approximate size to exclude small squares
    return lighter, darker


def red_majority_limit(red_majority, previous_red_majority, red_saturation_condition, direction='lighter'):
    delta_red_majority = red_majority - previous_red_majority
    if direction == 'lighter':
        # "the change in the value of (R-G-B)x320 is > 20"
        condition_a = np.where(delta_red_majority >= 20, 1, 0)
        return np.array(np.multiply(condition_a, red_saturation_condition), dtype=np.uint8)
    if direction == 'darker':
        # "the change in the value of (R-G-B)x320 is > 20"
        condition_a = np.where(delta_red_majority <= -20, 1, 0)
        return np.array(np.multiply(condition_a, red_saturation_condition), dtype=np.uint8)


def red_saturation_minimum(red_saturation, previous_red_saturation):
    max_red_saturation = np.maximum(red_saturation, previous_red_saturation)
    # "R/(R+ G + B) >= 0.8"
    threshold_red_saturation = np.where(max_red_saturation > 0.8, 1, 0)
    return threshold_red_saturation
