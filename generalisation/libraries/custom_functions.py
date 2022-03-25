import numpy as np
import re


def area_averages_max(flash_matrix, fragment_shape=(75, 100), threshold=None):
    m_y, m_x = flash_matrix.shape
    f_y, f_x = fragment_shape
    horizontal_sum = np.cumsum(flash_matrix, axis=0)
    rectangular_sum = np.cumsum(horizontal_sum, axis=1)
    big_rectangle = rectangular_sum[f_y - 1:m_y, f_x - 1:m_x]
    tall_rectangle = rectangular_sum[0:m_y - f_y + 1, f_x - 1:m_x]
    long_rectangle = rectangular_sum[f_y - 1:m_y, 0:m_x - f_x + 1]
    small_rectangle = rectangular_sum[0:m_y - f_y + 1, 0:m_x - f_x + 1]
    center_rectangle = big_rectangle - tall_rectangle - long_rectangle + small_rectangle
    max_value = np.max(np.divide(center_rectangle, f_y * f_x))
    if threshold is None:
        return max_value
    else:
        return max_value >= threshold


def count_flashes(flashes_lighter, flashes_darker, frame_rate=30):
    flashes_lighter[0], flashes_darker[0] = 0, 0
    channel1, channel2 = flashes_lighter[-(frame_rate - 1):], flashes_darker[-(frame_rate - 1):]
    both_channels = ''
    for i in range(len(channel1)):
        if channel1[i] and channel2[i]:
            both_channels += 'X'
        elif channel1[i]:
            both_channels += '1'
        elif channel2[i]:
            both_channels += '2'
    both_channels = re.sub('1+', '1', both_channels)
    both_channels = re.sub('2+', '2', both_channels)
    count = len(both_channels)
    return count
