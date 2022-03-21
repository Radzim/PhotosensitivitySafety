def sRGB(x):
    return max(x / 255 / 12.92, ((x / 255 + 0.055) / 1.055) ** 2.4)
