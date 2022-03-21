import numpy as np


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
