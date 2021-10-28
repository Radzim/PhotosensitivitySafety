import numpy as np


def calculate_relative_luminance(frame):
    s_rgb = np.divide(np.ndarray.copy(frame).astype(float), 255)
    x = np.maximum(np.divide(s_rgb, 12.92), np.power(np.divide(s_rgb + 0.055, 1.055), 2.4))
    return np.dot(x[..., :3], [0.0722, 0.7152, 0.2126])


def relative_luminance_limit(relative_luminance, previous_relative_luminance, lighter):
    delta_relative_luminance = relative_luminance - previous_relative_luminance
    if lighter:
        condition_a = np.where(delta_relative_luminance >= 0.1, 1, 0)
        condition_b = np.where(previous_relative_luminance <= 0.8, 1, 0)
    else:
        condition_a = np.where(delta_relative_luminance <= -0.1, 1, 0)
        condition_b = np.where(relative_luminance <= 0.8, 1, 0)
    return np.array(np.multiply(condition_a, condition_b), dtype=np.uint8)


def cross_reference_transitions(last_change, limit_relative_luminance_opposite):
    return np.array(last_change * limit_relative_luminance_opposite, dtype=int)


def update_last_flash(last_change, limit_relative_luminance, frame_rate):
    last_change = np.maximum(np.maximum(last_change - 1, 0), limit_relative_luminance * frame_rate)
    return last_change


def flash_frames_separator(flash_frames):
    flash_counts = np.bincount(np.ravel(flash_frames))
    return (flash_counts / sum(flash_counts))[1:]


def relative_luminance_both_limits(relative_luminance, previous_relative_luminance):
    lighter = relative_luminance_limit(relative_luminance, previous_relative_luminance, True)
    darker = relative_luminance_limit(relative_luminance, previous_relative_luminance, False)
    return lighter, darker


def update_both_last_flashes(last_changes, both_relative_luminance_limits, frame_rate):
    last_lighter, last_darker = last_changes
    limit_relative_luminance_lighter, limit_relative_luminance_darker = both_relative_luminance_limits
    last_lighter = update_last_flash(last_lighter, limit_relative_luminance_lighter, frame_rate)
    last_darker = update_last_flash(last_darker, limit_relative_luminance_darker, frame_rate)
    return last_lighter, last_darker


def cross_reference_both_transitions(last_changes, both_relative_luminance_limits):
    last_lighter, last_darker = last_changes
    limit_relative_luminance_lighter, limit_relative_luminance_darker = both_relative_luminance_limits
    lighter_darker_flash = cross_reference_transitions(last_lighter, limit_relative_luminance_darker)
    darker_lighter_flash = cross_reference_transitions(last_darker, limit_relative_luminance_lighter)
    return lighter_darker_flash, darker_lighter_flash


def flash_both_frames_separator(both_flashes):
    lighter_darker_flash, darker_lighter_flash = both_flashes
    lighter_darker_flash_counts = flash_frames_separator(lighter_darker_flash)
    darker_lighter_flash_counts = flash_frames_separator(darker_lighter_flash)
    return lighter_darker_flash_counts, darker_lighter_flash_counts


def flash_detect_printout(flash_counts, frame_count, frame_rate, thresholds):
    global_minimum_threshold, global_maximum_threshold = thresholds
    flash = False
    for frame_offset in range(len(flash_counts)):
        if flash_counts[frame_offset] >= global_maximum_threshold:
            flash = True
            print("FLASH @ ", frame_count - frame_rate + frame_offset, "-", frame_count)
        elif flash_counts[frame_offset] >= global_minimum_threshold:
            print("potential flash @ ", frame_count - frame_rate + frame_offset, "-", frame_count)
    return flash


def flash_detect_printout_both(flash_counts, frame_count, frame_rate, thresholds):
    lighter_darker_flash_counts, darker_lighter_flash_counts = flash_counts
    flash_detect_printout(lighter_darker_flash_counts, frame_count, frame_rate, thresholds)
    flash_detect_printout(darker_lighter_flash_counts, frame_count, frame_rate, thresholds)
