import numpy as np


def calculate_relative_luminance(frame):
    s_rgb = np.divide(np.ndarray.copy(frame).astype(float), 255)
    x = np.maximum(np.divide(s_rgb, 12.92), np.power(np.divide(s_rgb + 0.055, 1.055), 2.4))
    return np.dot(x[..., :3], [0.0722, 0.7152, 0.2126])


def relative_luminance_limits(relative_luminance, previous_relative_luminance):
    delta_relative_luminance = relative_luminance - previous_relative_luminance
    condition_a_lighter = np.where(delta_relative_luminance >= 0.1, 1, 0)
    condition_b_lighter = np.where(previous_relative_luminance <= 0.8, 1, 0)
    lighter = np.array(np.multiply(condition_a_lighter, condition_b_lighter), dtype=np.uint8)
    condition_a_darker = np.where(delta_relative_luminance <= -0.1, 1, 0)
    condition_b_darker = np.where(relative_luminance <= 0.8, 1, 0)
    darker = np.array(np.multiply(condition_a_darker, condition_b_darker), dtype=np.uint8)
    return lighter, darker


def update_last_flash(last_change, limit_relative_luminance, frame_rate):
    last_change = np.maximum(np.maximum(last_change - 1, 0), limit_relative_luminance * frame_rate)
    return last_change


def flash_frames_separator(flash_frames):
    flash_counts = np.bincount(np.ravel(flash_frames))
    return (flash_counts / sum(flash_counts))[1:]


def flash_detect_printout(flash_counts, frame_count, frame_rate, global_minimum_threshold, global_maximum_threshold):
    for frame_offset in range(len(flash_counts)):
        if flash_counts[frame_offset] >= global_maximum_threshold:
            print("DL FLASH @ ", frame_count - frame_rate + frame_offset, "-", frame_count)
        elif flash_counts[frame_offset] >= global_minimum_threshold:
            print("DL potential flash @ ", frame_count - frame_rate + frame_offset, "-", frame_count)
