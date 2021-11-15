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


def general_limits(relative_luminance, previous_relative_luminance):
    lighter = relative_luminance_limit(relative_luminance, previous_relative_luminance, direction='lighter')
    darker = relative_luminance_limit(relative_luminance, previous_relative_luminance, direction='darker')
    # "Exception: Flashing with "squares" smaller than 0.1 degree"
    # TODO: add average smoothing with approximate size to exclude small squares
    return lighter, darker


def relative_luminance_limit(relative_luminance, previous_relative_luminance, direction='lighter'):
    delta_relative_luminance = relative_luminance - previous_relative_luminance
    if direction == 'lighter':
        # "changes in relative luminance of 10% or more of the maximum relative luminance"
        condition_a = np.where(delta_relative_luminance >= 0.1, 1, 0)
        # "where the relative luminance of the darker image is below 0.80"
        condition_b = np.where(previous_relative_luminance <= 0.8, 1, 0)
        return np.array(np.multiply(condition_a, condition_b), dtype=np.uint8)
    if direction == 'darker':
        # "changes in relative luminance of 10% or more of the maximum relative luminance"
        condition_a = np.where(delta_relative_luminance <= -0.1, 1, 0)
        # "where the relative luminance of the darker image is below 0.80"
        condition_b = np.where(relative_luminance <= 0.8, 1, 0)
        return np.array(np.multiply(condition_a, condition_b), dtype=np.uint8)
